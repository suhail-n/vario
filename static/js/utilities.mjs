/**
 * Get the CSRF token from the cookies
 * @returns {string|null}
 */
export function getCsrfToken() {
    const csrfToken = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken'));
    if (!csrfToken) {
        console.error("CSRF token not found");
        return null;
    }
    console.log(`CSRF token: ${csrfToken}`);
    return csrfToken.split('=')[1];
}