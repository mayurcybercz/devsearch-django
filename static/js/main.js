//pagination and search fix 
    
    // to get search form and page links
    let searchForm=document.getElementById('searchForm')
    let pageLinks =document.getElementsByClassName('page-link')

    //ensure search form exists, add eventhandler for
    if(searchForm){
        for(let i=0;pageLinks.length>i;i++){
            pageLinks[i].addEventListener('click',function(e){
                e.preventDefault();
                
                //get data attributes
                let page=this.dataset.page;
                //add hidden search input to form
                searchForm.innerHTML+=`<input value=${page} name="page" hidden/>`;
                //submit form
                searchForm.submit();
            })
        }
    }


//  tag remove fix
let tags = document.getElementsByClassName('project-tag')

for (let i = 0; tags.length > i; i++) {
    tags[i].addEventListener('click', (e) => {
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project

        // console.log('TAG ID:', tagId)
        // console.log('PROJECT ID:', projectId)

        fetch('http://localhost:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'project': projectId, 'tag': tagId })
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })

    })
}

// add error handling to event listeners