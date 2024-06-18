document.querySelectorAll('.dialog-button').forEach(button => {
    button.addEventListener('click', () => {
        alert(`You clicked button ${button.textContent}`);
    });
});
