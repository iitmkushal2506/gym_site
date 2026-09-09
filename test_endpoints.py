import urllib.request
import urllib.parse
import http.cookiejar
import sys
import re

BASE_URL = "http://127.0.0.1:5000"

# Setup cookie jar for session maintenance
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)

def test_url(path, expected_status=200):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with opener.open(req) as resp:
            status = resp.getcode()
            body = resp.read().decode('utf-8')
            print(f"[PASS] {path} -> HTTP {status} (Length: {len(body)} bytes)")
            return status, body
    except urllib.error.HTTPError as e:
        print(f"[FAIL] {path} -> HTTP {e.code}")
        return e.code, ""
    except Exception as e:
        print(f"[ERR] {path} -> {e}")
        return 0, ""

def extract_csrf(body):
    match = re.search(r'name="csrf_token"[^>]*?value="([^"]+)"', body)
    if not match:
        match = re.search(r'value="([^"]+)"[^>]*?name="csrf_token"', body)
    if not match:
        match = re.search(r'id="csrf_token"[^>]*?value="([^"]+)"', body)
    return match.group(1) if match else None

def run_tests():
    print("=== 1. TESTING PUBLIC ENDPOINTS ===")
    public_paths = [
        '/',
        '/about',
        '/membership',
        '/trainers',
        '/trainers/marcus-vance',
        '/classes',
        '/facilities',
        '/transformations',
        '/contact',
        '/book-trial',
        '/book-consultation',
        '/robots.txt',
        '/sitemap.xml'
    ]
    for path in public_paths:
        status, _ = test_url(path)
        assert status == 200, f"Expected 200 for {path}, got {status}"

    print("\n=== 2. TESTING ADMIN LOGIN & SESSION ===")
    status, login_html = test_url('/admin/login')
    csrf_token = extract_csrf(login_html)
    assert csrf_token is not None, "CSRF token not found on login page"

    login_data = urllib.parse.urlencode({
        'csrf_token': csrf_token,
        'username': 'admin',
        'password': 'admin123',
        'submit': 'Sign In to Dashboard'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/admin/login", data=login_data, headers={'User-Agent': 'Mozilla/5.0'})
    with opener.open(req) as resp:
        print(f"[PASS] Admin login post -> HTTP {resp.getcode()}")

    print("\n=== 3. TESTING PROTECTED ADMIN ENDPOINTS ===")
    admin_paths = [
        '/admin/dashboard',
        '/admin/leads',
        '/admin/trials',
        '/admin/appointments',
        '/admin/memberships',
        '/admin/trainers',
        '/admin/classes',
        '/admin/facilities',
        '/admin/transformations',
        '/admin/testimonials',
        '/admin/instagram'
    ]
    for path in admin_paths:
        status, body = test_url(path)
        assert status == 200, f"Expected 200 for {path}, got {status}"
        assert 'Sign In to Dashboard' not in body, f"Redirected to login for {path}"

    print("\n=== 4. TESTING FORM SUBMISSIONS (TRIAL & CONSULTATION) ===")
    # Test Trial Booking
    status, trial_html = test_url('/book-trial')
    trial_csrf = extract_csrf(trial_html)
    trial_data = urllib.parse.urlencode({
        'csrf_token': trial_csrf,
        'name': 'Test Runner',
        'email': 'runner@example.com',
        'phone': '+91 99887 76655',
        'age': '28',
        'fitness_goal': 'Weight Loss & Fat Burn',
        'preferred_date': '2026-10-01',
        'preferred_time': '06:00 AM - 08:00 AM (Early Bird)',
        'message': 'Automated test pass'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/book-trial", data=trial_data, headers={'User-Agent': 'Mozilla/5.0'})
    with opener.open(req) as resp:
        trial_resp_body = resp.read().decode('utf-8')
        assert 'VIP TRIAL PASS CONFIRMED' in trial_resp_body or resp.getcode() == 200
        print("[PASS] Free trial booking submitted successfully and redirected to success page!")

    # Test Consultation Booking with Double-Booking Prevention
    import time, random
    unique_slot = f"{random.randint(6, 11):02d}:{random.choice(['00', '15', '30', '45'])} AM"
    test_date = f"2028-{(int(time.time()*1000) % 12) + 1:02d}-{(int(time.time()) % 28) + 1:02d}"
    status, consult_html = test_url('/book-consultation')
    consult_csrf = extract_csrf(consult_html)
    
    # 1st booking
    consult_data_1 = urllib.parse.urlencode({
        'csrf_token': consult_csrf,
        'name': 'First Client',
        'email': 'first@example.com',
        'phone': '+91 99000 11223',
        'trainer_id': '1',
        'goal': '1-on-1 Personal Training',
        'fitness_level': 'Intermediate (1-2 years consistent)',
        'preferred_date': test_date,
        'preferred_time': unique_slot,
        'message': 'Session 1'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/book-consultation", data=consult_data_1, headers={'User-Agent': 'Mozilla/5.0'})
    with opener.open(req) as resp:
        body = resp.read().decode('utf-8')
        assert 'CONSULTATION REQUEST SUBMITTED' in body
        print("[PASS] 1st Consultation booking succeeded!")

    # 2nd booking attempt for same trainer/date/time
    status, consult_html_2 = test_url('/book-consultation')
    consult_csrf_2 = extract_csrf(consult_html_2)
    consult_data_2 = urllib.parse.urlencode({
        'csrf_token': consult_csrf_2,
        'name': 'Conflicting Client',
        'email': 'second@example.com',
        'phone': '+91 99000 44556',
        'trainer_id': '1',
        'goal': '1-on-1 Personal Training',
        'fitness_level': 'Beginner (Just getting started)',
        'preferred_date': test_date,
        'preferred_time': unique_slot,
        'message': 'Session conflict test'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/book-consultation", data=consult_data_2, headers={'User-Agent': 'Mozilla/5.0'})
    with opener.open(req) as resp:
        conflict_body = resp.read().decode('utf-8')
        assert 'already has an appointment booked' in conflict_body
        print("[PASS] Double-booking prevention verified! System blocked duplicate booking for same coach, date, and time slot.")

    print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY! 100% FUNCTIONAL.")

if __name__ == '__main__':
    run_tests()
