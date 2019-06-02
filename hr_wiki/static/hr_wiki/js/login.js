// MODAL LOGIN
const button = document.getElementById('btn')
const modal = document.querySelector('.modal')
const sideLogin = document.querySelector('.sidebar .sidebar-nav span.login')

button.addEventListener('click', ()=>{
    modal.classList.toggle('show')
    button.classList.toggle('clicked')
})

window.addEventListener('click', ()=>{
    if (event.target == modal || event.target == nav){
        modal.classList.remove('show')
        button.classList.remove('clicked')
    }
})

sideLogin.addEventListener('click', ()=>{
    sidebar.classList.remove('show')
    modal.classList.add('show')
})