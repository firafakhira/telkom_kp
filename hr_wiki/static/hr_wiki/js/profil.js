// MODAL PROFIL
profil = document.getElementById('profil')
modal = document.querySelector('.modal')
nav = document.querySelector('nav')

profil.addEventListener('click', ()=>{
    modal.classList.toggle('show')
})

window.addEventListener('click', ()=>{
    if (event.target == modal || event.target == nav){
        modal.classList.toggle('show')
    }
})