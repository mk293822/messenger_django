 // JavaScript to toggle sidebar visibility
      function toggleSidebar() {
        var sidebar = document.getElementById("sidebar");
        sidebar.classList.toggle("active");// Toggle 'active' class to show/hide sidebar
        console.log('Hello world');
}
      
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
    console.log('Hello')
  });
}

window.onload = function () {
        const messagesContainer = document.querySelector(".container");
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
};
      



// like message action
const likesvg = `
   <svg width="3pc" height="3pc" fill="#2050ca" viewBox="0 -0.5 21 21" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
 
    <g id="Page-1"  fill-rule="evenodd">
        <g id="Dribbble-Light-Preview" transform="translate(-259.000000, -760.000000)" fill="#2050ca">
            <g id="icons" transform="translate(56.000000, 160.000000)">
                <path d="M203,620 L207.200006,620 L207.200006,608 L203,608 L203,620 Z M223.924431,611.355 L222.100579,617.89 C221.799228,619.131 220.638976,620 219.302324,620 L209.300009,620 L209.300009,608.021 L211.104962,601.825 C211.274012,600.775 212.223214,600 213.339366,600 C214.587817,600 215.600019,600.964 215.600019,602.153 L215.600019,608 L221.126177,608 C222.97313,608 224.340232,609.641 223.924431,611.355 L223.924431,611.355 Z" id="like-[#1385]">

</path>
            </g>
        </g>
    </g>
</svg>
` 
const likeBtn = document.querySelector('.like__container');
const roomId = document.getElementById('roomId').value;
const url1 = `/like_send/${roomId}/`

likeBtn.addEventListener('click', () => {
  //console.log('haha')
  fetch(url1, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: new URLSearchParams({
      svg: likesvg
    })
  }).then(response => response.text()).then(data => {
    console.log(`success${data}`);
  }).catch(error => {
    console.error(error);
  });
  location.reload();
});

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++){
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null
}

let messageButtons = document.querySelectorAll('.message__button');

messageButtons.forEach(element => {
  if (element.querySelector('svg')) {
    element.style.background = 'none';
    element.style.border = 'none';
  } 
});


// Image send read file

const imageBtn = document.querySelector('.gallery__container');
const imageInput = document.getElementById('image_input');

imageBtn.addEventListener('click', () => {
  imageInput.click()
});

imageInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append('img', file);
  formData.append('room_id', roomId);

  const url2 = `/image_send/${roomId}/`;

  fetch(url2, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: formData
  }).then(response => response.text()).then(data => {
    console.log(`success: ${data}`);
    location.reload();  // Consider updating the UI instead of reloading
  }).catch(error => {
    console.error('Error:', error);
  });
});

