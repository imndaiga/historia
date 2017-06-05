
export function createModalData (headerIcon, header, subject, message, color, type, submitMessage, submitUrl, searchUrl) {
  return {
    header: header || '',
    headerIcon: headerIcon || '',
    subject: subject || '',
    message: message || '',
    color: color || 'default',
    type: type || '',
    submitMessage: submitMessage || '',
    submitUrl: submitUrl || '',
    searchUrl: searchUrl || ''
  }
}

export const errors = {
  connection: createModalData('exclamation-circle', 'Ooops', 'An error occured!', 'Something went wrong while retreiving data.', 'red', 'alert'),
  action: createModalData('exclamation-circle', 'Ooops', 'An error occured!', 'Something went wrong while performing action.', 'red', 'alert'),
  development: createModalData('exclamation-circle', 'Coming Soon!', 'Under Development!', 'This feature is ready yet.', null, 'alert')
}
