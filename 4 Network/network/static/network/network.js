
document.addEventListener('DOMContentLoaded', function() {


    document.querySelectorAll('.edit').forEach(button => {
        button.addEventListener('click', function(){

            const tweet_content = this.getAttribute('data-info');
            const tweetDiv = button.closest('.tweet');
            const contentDiv = tweetDiv.querySelector('.content');
            const editFormDiv = tweetDiv.querySelector('.edit_content');
            const textarea = editFormDiv.querySelector('textarea');

            contentDiv.style.display = 'none';
            editFormDiv.style.display = 'block';

            textarea.value = `${tweet_content}`;
        });
    });
  

    document.querySelectorAll('.save_edit').forEach(button => {
        button.addEventListener('click', function(){
            const tweetDiv = button.closest('.tweet');
            const tweetId = tweetDiv.getAttribute('data-id');
            const textarea = tweetDiv.querySelector('textarea');
            const content = textarea.value;

            fetch(`/edit/${tweetId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: content
                })
              })
        });
    });



    document.querySelectorAll('.like').forEach(button => {
        button.addEventListener('click', function(){
            const tweetDiv = button.closest('.tweet');
            const tweetId = tweetDiv.getAttribute('data-id');

            fetch(`/like/${tweetId}`, {
                method: 'PUT',
                body: JSON.stringify({})
              })
            .then(response => response.json())  
            .then(data => {
                tweetDiv.querySelector('.like-count-value').textContent = data.likes;
            });

        });
    });



  });


