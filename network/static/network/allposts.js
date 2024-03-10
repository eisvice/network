document.addEventListener('DOMContentLoaded', function() {
    const currentURL = window.location.href.replace('http://127.0.0.1:8000', '');
    console.log(currentURL);
    console.log(document.querySelector('#follow'));
    if ((followButton = document.querySelector('#follow')) !== null) {
        followButton.addEventListener('click', function(event) {
            event.preventDefault();
            const followed = followButton.value;
            let follower;
            console.log(followed);
            if (followed === 'Follow') {
                console.log('now you are being followed');
                followButton.value = 'Unfollow';
                follower = true;
                console.log(follower);
                document.querySelector('#followers-count').innerHTML = parseInt(document.querySelector('#followers-count').innerHTML) + 1;
            }  else if (followed === 'Unfollow') {
                console.log('now you are being unfollowed');
                followButton.value = 'Follow';
                follower = false;
                console.log(follower);
                document.querySelector('#followers-count').innerHTML = parseInt(document.querySelector('#followers-count').innerHTML) - 1;
            }
            fetch(currentURL, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({follower: follower})
            })
            .then(response => response.json())
            .then(result => {
              // Print result
              console.log(result);
            })
            .then(() => {
                followButton.blur();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        })
    }
    
    document.querySelectorAll('.like-post').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.postId;
            const liked = this.dataset.liked === 'true';
            const likesCountElement = document.querySelector(`#likes-count-${postId}`);
            if (!liked) {
                likesCountElement.textContent = parseInt(likesCountElement.textContent) + 1;
                this.dataset.liked = 'true';
                button.innerHTML = '❤️';
            } else {
                likesCountElement.textContent = parseInt(likesCountElement.textContent) - 1;
                this.dataset.liked = 'false';
                button.innerHTML = '🤍';
            }
            fetch(currentURL ,{
                method: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({post_id: postId, liked: this.dataset.liked})
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    document.querySelectorAll('.edit-post').forEach(button => {
        button.addEventListener('click', function() {
            // event.preventDefault();
            console.log('you clicked');
            const postID = this.dataset.postId;
            const twitt = button.parentElement;
            console.log(postID);
            console.log(button.parentElement.querySelector('.body'));
            const body = button.parentElement.querySelector('.body');
            const bodyEdit = document.createElement('textarea');
            bodyEdit.innerHTML = body.innerHTML;
            body.replaceWith(bodyEdit);
            button.style.display = 'none';
            const saveBtn = document.createElement('button');
            const cancelBtn = document.createElement('button');
            saveBtn.className = 'btn btn-primary save-button';
            saveBtn.innerHTML = 'Save';
            cancelBtn.className = 'btn btn-primary cancel-button';
            cancelBtn.innerHTML = 'Cancel';

            twitt.append(saveBtn, cancelBtn);
            cancelBtn.addEventListener('click', function() {
                saveBtn.style.display = 'none';
                cancelBtn.style.display = 'none';
                button.style.display = 'block';
                bodyEdit.replaceWith(body);
            });
            saveBtn.addEventListener('click', function(event) {
                event.preventDefault();
                body.innerHTML = bodyEdit.value;
                saveBtn.style.display = 'none';
                cancelBtn.style.display = 'none';
                button.style.display = 'block';
                console.log(bodyEdit.value);
                console.log(body.innerHTML);
                bodyEdit.replaceWith(body);
                fetch('' ,{
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        post_id: postID,
                        author: twitt.user,
                        body: body
                    })
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            })
        });
    });
});


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