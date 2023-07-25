// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });


// let alertWrapper = document.querySelector('.alert')
// let alertClose = document.querySelector('.alert__close')

// if (alertWrapper) {
//   alertClose.addEventListener('click', () =>
//     alertWrapper.style.display = 'none'
//   )
// }

document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();

  // Wrap the event listener setup inside the DOMContentLoaded event handler
  let alertWrappers = document.querySelectorAll('.alert');

  // Use event delegation to handle the close button click event
  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('alert__close')) {
      event.target.closest('.alert').style.display = 'none';
    }
  });
});

