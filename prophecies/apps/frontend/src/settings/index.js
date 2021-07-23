export default {
  apiUrl: '/api/v1',
  defaultLocale: 'en',
  helpLink: 'https://github.com/ICIJ/prophecies/issues/new',
  locales: [
    {
      key: 'en',
      label: 'English'
    }
  ],
  loginUrl: '/login/xemx/?next=/',
  logoutUrl: '/admin/logout/?next=/',
  variantsMap: {
    success: 'success',
    ok: 'success',
    done: 'success',
    danger: 'danger',
    error: 'danger',
    fail: 'danger',
    failed: 'danger',
    failure: 'danger',
    info: 'info',
    pending: 'info',
    queued: 'info',
    running: 'info',
    warning: 'warning',
    cancelled: 'warning'
  }
}
