// MODAL PROFIL
const profil = document.getElementById('profil')
const modal = document.querySelector('.modal')

profil.addEventListener('click', ()=>{
    modal.classList.toggle('show')
})

window.addEventListener('click', ()=>{
    if (event.target == modal || event.target == nav){
        modal.classList.remove('show')
    }
})