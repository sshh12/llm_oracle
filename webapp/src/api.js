export const APP_HOST =
  window.location.hostname === 'localhost' ? 'http://localhost:5000' : '';

export function get(path) {
  return fetch(`${APP_HOST}/api/${path}`).then(resp => resp.json());
}
