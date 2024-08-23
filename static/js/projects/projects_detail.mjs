import { getCsrfToken } from "../utilities.mjs";

/**
 * 
 * @param {string} toggleId
 */
// string toggleid
export async function updateToggle(toggleId) {
    const csrfToken = getCsrfToken();
    return fetch(`/projects/api/internal/toggles/${toggleId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    });
}

export function setFeatureToggleEventListener() {
    let checkboxes = document.querySelectorAll("input[name='feature-toggle']");
    for (let checkbox of checkboxes) {
        checkbox.addEventListener('change', function () {
            let toggle_id = this.id;
            updateToggle(toggle_id).catch(error => console.error("Error:", error));
        })
    };
}