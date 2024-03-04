document.addEventListener('DOMContentLoaded', function() {

    // load_posts();
    document.querySelector('#post-content').value = '';
    document.querySelector('#submit-new-post').onclick = function(event) {
        submitNewPost(event);
    };
});


function load_posts() {
    fetch('')
    .then(response => response.json())
    .then(posts => {})
}


function submitNewPost(event) { 
    // Prevent the default form submission
    event.preventDefault(); 

    // Select the form element
    const form = document.querySelector('form');
    
    // Serialize form data
    const formData = new FormData(form);
    formData.append('submit-new-post', 'Post');
        
    // Make a POST request to the server
    fetch('', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // You need to implement this function to get the CSRF token
        },
        body: formData // Sending a flag that the "submit-new-post" button was clicked
    })
    .then(response => {
        if (response.status === 201) {
            return response.json()
        } else {
            throw new Error('Failed to submit new post');
        }
    })
    .then(data => {
        console.log(data); // Logging the message to the console
        const twitt = document.createElement('div');
        twitt.className = "twitt";
        twitt.innerHTML = `${data.twitt.user} ${data.twitt.body} ${data.twitt.timestamp}`; 
        const twitts = document.querySelector('#twitts');
        twitts.prepend(twitt);
        document.querySelector('#post-content').value = ''
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
  

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}