/**
 * IRONFORGE FITNESS - ADMIN DASHBOARD JAVASCRIPT
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.admin-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });
  }

  // 2. Generic Delete Confirmation Modal
  const deleteModalEl = document.getElementById('deleteConfirmModal');
  if (deleteModalEl) {
    const deleteForm = document.getElementById('deleteModalForm');
    const deleteItemName = document.getElementById('deleteItemName');
    const deleteButtons = document.querySelectorAll('.btn-delete-trigger');

    deleteButtons.forEach(btn => {
      btn.addEventListener('click', function () {
        const actionUrl = this.getAttribute('data-action');
        const itemName = this.getAttribute('data-name') || 'this item';
        
        if (deleteForm) deleteForm.action = actionUrl;
        if (deleteItemName) deleteItemName.textContent = itemName;

        const modal = new bootstrap.Modal(deleteModalEl);
        modal.show();
      });
    });
  }

  // 3. Lead Notes Modal Handler
  const notesModalEl = document.getElementById('leadNotesModal');
  if (notesModalEl) {
    const notesButtons = document.querySelectorAll('.btn-notes-trigger');
    const notesForm = document.getElementById('leadNoteForm');
    const notesLeadTitle = document.getElementById('notesLeadTitle');
    const notesHistoryContainer = document.getElementById('notesHistoryContainer');

    notesButtons.forEach(btn => {
      btn.addEventListener('click', function () {
        const leadType = this.getAttribute('data-type');
        const leadId = this.getAttribute('data-id');
        const leadName = this.getAttribute('data-name');
        const notesJson = this.getAttribute('data-notes');

        if (notesLeadTitle) notesLeadTitle.textContent = `Notes for ${leadName} (${leadType})`;
        if (notesForm) notesForm.action = `/admin/leads/${leadType.toUpperCase()}/${leadId}/note`;

        if (notesHistoryContainer) {
          notesHistoryContainer.innerHTML = '';
          try {
            const notes = JSON.parse(notesJson || '[]');
            if (notes.length === 0) {
              notesHistoryContainer.innerHTML = '<p class="text-muted small">No internal notes added yet.</p>';
            } else {
              notes.forEach(n => {
                const noteCard = document.createElement('div');
                noteCard.className = 'p-3 mb-2 rounded bg-dark border border-secondary border-opacity-25';
                noteCard.innerHTML = `
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="badge bg-primary bg-opacity-25 text-primary small">${n.author || 'Admin'}</span>
                    <span class="text-muted small">${n.date}</span>
                  </div>
                  <p class="mb-0 text-light small">${n.note}</p>
                `;
                notesHistoryContainer.appendChild(noteCard);
              });
            }
          } catch (e) {
            notesHistoryContainer.innerHTML = '<p class="text-muted small">No internal notes.</p>';
          }
        }

        const modal = new bootstrap.Modal(notesModalEl);
        modal.show();
      });
    });
  }
});
