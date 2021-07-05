const submit = document.getElementById('submit');
submit.addEventListener("click",hideList);

const progDrop = document.querySelectorAll('.program-dropdown-wrapper');
const levDrop = document.querySelectorAll('.level-dropdown-wrapper');
const searchBar = document.getElementById('searchBar');
const listItems= document.querySelectorAll('.course-list-item');
var listItemsId= [];
var i=0;
listItems.forEach(item => {
    listItemsId[i]=item.id;
    i=i+1;
});

var progDropData=[];

function hideList(){
  var courseList=document.getElementById('course-list')
  listItems.forEach(item => {
    courseList.appendChild(item)
  });

  progDropData=[]
  var i=0
    progDrop.forEach(prog => {
      if (prog.childNodes[5].childNodes[0].childNodes){
          const progDropChildren=prog.childNodes[5].childNodes[0].childNodes
          progDropChildren.forEach(progDropChild => {
            if (progDropChild.dataset.key){
            progDropData[i]=progDropChild.dataset.key
            i=i+1;
          }
          });

      }
    });


    var levelVal;
    levDrop.forEach(lev => {
      levelVal=lev.childNodes[5].childNodes[0].innerText;
    });
    if(searchBar.value){keywordVal=searchBar.value.split(',');}

    listItemsId.forEach(id => {
        removeElement(id);
    });


    listItems.forEach(item1 => {
      var check=true;
      progDropData.forEach(dataItem => {
        if (!item1.classList.contains(dataItem)){check=false}
      });
      if (levelVal!=="Select an Option..."){
        if (!item1.classList.contains(levelVal)){check=false}
      }
      if (searchBar.value){
        keywordVal.forEach(word => {
            if (!item1.textContent.toLowerCase().includes(word.toLowerCase())){check=false}
        });
      }

      if (check){courseList.appendChild(item1)}

    });
}

function removeElement(elementId) {
    // Removes an element from the document
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}
