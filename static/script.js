
function form_check_nav(){
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].addEventListener('click', function() {
            if (this.checked) {
                for (var j = 0; j < checkboxes.length; j++) {
                    if (checkboxes[j] !== this) {
                        checkboxes[j].checked = false;
                    }
                }
            }
        });
    };
    const nav = document.getElementById('nav');
     window.addEventListener('scroll', ()=>{
     if(window.scrollY> 100){
        nav.classList.add('navactive')
    }else{
        nav.classList.remove('navactive')
    }
    })

    


}

form_check_nav()

const likeButton = document.querySelector('#like-button');
const likeCount = document.querySelector('#like-count');

likeButton.addEventListener('click', async (event) => {
  event.preventDefault();
  const postId = likeButton.dataset.userId;
  const response = await fetch(`/post/${postId}/like`, { method: 'POST' });
  const data = await response.json();
  likeCount.textContent = data.like_count;
});


function validate(){
    var  content = document.getElementById('content').value;

    if( content == " "){
      alert("fill in the text");
      return false;
    }else{
        return true
    }

}


// const like = document.getElementById("like");
// like.addEventListener('click',()=>{
// function like(){
//     if(like.style.background=="black"){
//         like.style.background=" #4CAF50";
//     }else if(like.style.background==" #4CAF50"){
//         like.style.background="black"
//     }else{
//         like.style.background=" #4CAF50";
//     }
// }

// like();
// })

 
  

  
//   function makeItalic() {
//       const textarea = document.getElementById('myTextarea');
//       const selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
//       const newText = '<i>' + selectedText + '</i>';
//       const beforeText = textarea.value.substring(0, textarea.selectionStart);
//       const afterText = textarea.value.substring(textarea.selectionEnd, textarea.value.length);
//       textarea.value = beforeText + newText + afterText;
//     }


