const sidebar = document.querySelector('.sidebar')
const hamburger = document.querySelector('.hamburger-icon')
const nav = document.querySelector('nav')

hamburger.addEventListener('click', ()=>{
    sidebar.classList.toggle('show')
    modal.classList.remove('show')
})

window.addEventListener('click', ()=>{
    if (event.target == sidebar || event.target == nav){
        sidebar.classList.remove('show')
    }
})