/**
 * Enhanced Tag Picker Component JavaScript
 *
 * Provides interactive tag selection with:
 * - Autocomplete/type-ahead search
 * - Visual pill display for selected tags
 * - Browse modal for viewing all tags
 */

// Add a tag to the picker
function addTag(fieldName, tagId) {
    const tags = window.tagPickerData[fieldName];
    const tag = tags.find(t => t.id === tagId);

    if (!tag) return;

    // Check if already selected
    const hiddenInputs = document.querySelectorAll(`input[data-tag-input="${fieldName}"]`);
    for (let input of hiddenInputs) {
        if (input.value === String(tagId)) {
            return; // Already selected
        }
    }

    // Add hidden input for form submission
    const form = document.querySelector(`#${fieldName}_input`).closest('form');
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = fieldName;
    hiddenInput.value = tagId;
    hiddenInput.setAttribute('data-tag-input', fieldName);
    form.appendChild(hiddenInput);

    // Add pill to UI
    const pillsContainer = document.getElementById(`${fieldName}_pills`);
    const pill = document.createElement('span');
    pill.className = 'tag-pill';
    pill.setAttribute('data-tag-id', tagId);
    pill.innerHTML = `
        ${tag.value}
        <button type="button" class="tag-pill-remove" onclick="removeTag('${fieldName}', ${tagId})">×</button>
    `;
    pillsContainer.appendChild(pill);

    // Clear input
    document.getElementById(`${fieldName}_input`).value = '';
    document.getElementById(`${fieldName}_dropdown`).style.display = 'none';

    // Update modal checkbox if open
    const modal = document.getElementById(`${fieldName}_modal`);
    if (modal) {
        const checkbox = modal.querySelector(`input[type="checkbox"][value="${tagId}"]`);
        if (checkbox) checkbox.checked = true;
    }
}

// Remove a tag from the picker
function removeTag(fieldName, tagId) {
    // Remove hidden input
    const hiddenInputs = document.querySelectorAll(`input[data-tag-input="${fieldName}"]`);
    for (let input of hiddenInputs) {
        if (input.value === String(tagId)) {
            input.remove();
            break;
        }
    }

    // Remove pill from UI
    const pillsContainer = document.getElementById(`${fieldName}_pills`);
    const pill = pillsContainer.querySelector(`[data-tag-id="${tagId}"]`);
    if (pill) pill.remove();

    // Update modal checkbox if open
    const modal = document.getElementById(`${fieldName}_modal`);
    if (modal) {
        const checkbox = modal.querySelector(`input[type="checkbox"][value="${tagId}"]`);
        if (checkbox) checkbox.checked = false;
    }
}

// Filter tags based on input
function filterTags(fieldName) {
    const input = document.getElementById(`${fieldName}_input`);
    const query = input.value.toLowerCase().trim();
    const dropdown = document.getElementById(`${fieldName}_dropdown`);

    if (query.length < 2) {
        dropdown.style.display = 'none';
        return;
    }

    const tags = window.tagPickerData[fieldName];
    const filtered = tags.filter(tag =>
        tag.value.toLowerCase().includes(query) ||
        tag.category.toLowerCase().includes(query)
    ).slice(0, 10); // Limit to 10 results

    if (filtered.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    // Build dropdown HTML
    dropdown.innerHTML = filtered.map(tag => `
        <div class="tag-autocomplete-item" onclick="addTag('${fieldName}', ${tag.id})">
            <span class="tag-autocomplete-category">${tag.category.replace(/_/g, ' ')}</span>
            <span class="tag-autocomplete-value">${tag.value}</span>
        </div>
    `).join('');

    dropdown.style.display = 'block';
}

// Open the tag browser modal
function openTagBrowser(fieldName) {
    const modal = document.getElementById(`${fieldName}_modal`);
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

// Close the tag browser modal
function closeTagBrowser(fieldName) {
    const modal = document.getElementById(`${fieldName}_modal`);
    modal.style.display = 'none';
    document.body.style.overflow = ''; // Restore scrolling
}

// Close modal when clicking backdrop
function closeModalOnBackdrop(event, fieldName) {
    if (event.target.classList.contains('tag-browser-modal')) {
        closeTagBrowser(fieldName);
    }
}

// Toggle tag selection in modal
function toggleTagInModal(fieldName, tagId) {
    const checkbox = event.target;

    if (checkbox.checked) {
        addTag(fieldName, tagId);
    } else {
        removeTag(fieldName, tagId);
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdowns = document.querySelectorAll('.tag-autocomplete-dropdown');
    dropdowns.forEach(dropdown => {
        const input = dropdown.previousElementSibling.querySelector('.tag-picker-input');
        if (input && !input.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    });
});
