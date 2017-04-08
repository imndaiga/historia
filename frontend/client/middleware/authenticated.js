export default function ({ redirect }) {
  if (process.browser) {
    if (!localStorage.getItem('id_token')) {
      redirect('/')
    }
  }
}
