/*
===============================================================

Hi! Welcome to my little playground!

My name is Tobias Bogliolo. 'Open source' by default and always 'responsive',
I'm a publicist, visual designer and frontend developer based in Barcelona. 

Here you will find some of my personal experiments. Sometimes usefull,
sometimes simply for fun. You are free to use them for whatever you want 
but I would appreciate an attribution from my work. I hope you enjoy it.

===============================================================
*/

$(document).ready(function(){
    //Show contextmenu:
    $('.items').contextmenu(function(e){
      // var item = $(this).text()
      var item = $(this).text()
      allPath = $(location).attr('pathname')
      host = $(location).attr('host')
      
      var context = $('.contextmenu li a')
      allPathArry = allPath.split("/")
      needPath1 = allPathArry.splice(1, 2).join('/')
      needPath2 = allPathArry.splice(2, allPathArry.length-2).join('/')

      context[0].href = "http://" + host + '/' + needPath1 +"/delete/" + needPath2 + item
      context[1].href = "http://" + host + '/' + needPath1 +"/log/" + needPath2 + item
      //Get window size:
      var winWidth = $(document).width();
      var winHeight = $(document).height();
      //Get pointer position:
      var posX = e.pageX;
      var posY = e.pageY;
      //Get contextmenu size:
      var menuWidth = $(".contextmenu").width();
      var menuHeight = $(".contextmenu").height();
      //Security margin:
      var secMargin = 10;
      //Prevent page overflow:
      if(posX + menuWidth + secMargin >= winWidth
      && posY + menuHeight + secMargin >= winHeight){
        //Case 1: right-bottom overflow:
        posLeft = posX - menuWidth - secMargin + "px";
        posTop = posY - menuHeight - secMargin + "px";
      }
      else if(posX + menuWidth + secMargin >= winWidth){
        //Case 2: right overflow:
        posLeft = posX - menuWidth - secMargin + "px";
        posTop = posY + secMargin + "px";
      }
      else if(posY + menuHeight + secMargin >= winHeight){
        //Case 3: bottom overflow:
        posLeft = posX + secMargin + "px";
        posTop = posY - menuHeight - secMargin + "px";
      }
      else {
        //Case 4: default values:
        posLeft = posX + secMargin + "px";
        posTop = posY + secMargin + "px";
      };
      //Display contextmenu:
      $(".contextmenu").css({
        "left": posLeft,
        "top": posTop
      }).show();
      //Prevent browser default contextmenu.

      return false;
    });
    //Hide contextmenu:
    $(document).click(function(){
      $(".contextmenu").hide();
    });
  });

$(document).ready(function(){
  //Show contextmenu:
  $('.itemsPrivate').contextmenu(function(e){
    
    var item = $(this).text()
    allPath = $(location).attr('pathname')
    host = $(location).attr('host')
    
    var context = $('.contextmenuPrivate li a')
    
    allPathArry = allPath.split("/")
    needPath1 = allPathArry.splice(1, 2).join('/')
    needPath2 = allPathArry.splice(2, allPathArry.length-2).join('/')

    context[0].href = "http://" + host + '/' + needPath1 +"/delete/" + needPath2 + item
    //Get window size:
    var winWidth = $(document).width();
    var winHeight = $(document).height();
    //Get pointer position:
    var posX = e.pageX;
    var posY = e.pageY;
    //Get contextmenu size:
    var menuWidth = $(".contextmenuPrivate").width();
    var menuHeight = $(".contextmenuPrivate").height();
    //Security margin:
    var secMargin = 10;
    //Prevent page overflow:
    if(posX + menuWidth + secMargin >= winWidth
    && posY + menuHeight + secMargin >= winHeight){
      //Case 1: right-bottom overflow:
      posLeft = posX - menuWidth - secMargin + "px";
      posTop = posY - menuHeight - secMargin + "px";
    }
    else if(posX + menuWidth + secMargin >= winWidth){
      //Case 2: right overflow:
      posLeft = posX - menuWidth - secMargin + "px";
      posTop = posY + secMargin + "px";
    }
    else if(posY + menuHeight + secMargin >= winHeight){
      //Case 3: bottom overflow:
      posLeft = posX + secMargin + "px";
      posTop = posY - menuHeight - secMargin + "px";
    }
    else {
      //Case 4: default values:
      posLeft = posX + secMargin + "px";
      posTop = posY + secMargin + "px";
    };
    //Display contextmenu:
    $(".contextmenuPrivate").css({
      "left": posLeft,
      "top": posTop
    }).show();
    //Prevent browser default contextmenu.

    return false;
  });
  //Hide contextmenu:
  $(document).click(function(){
    $(".contextmenuPrivate").hide();
  });
});

  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.file-droppable').forEach(function(droppable) {
      var originalText = droppable.querySelector('div').innerHTML;
      var input = droppable.querySelector('input');
      var fileChanged = function() {
        var files = input.files;
        if (files.length) {
          droppable.querySelector('span').style.display = 'block';
          droppable.querySelector('div').innerHTML = '';
          for (var i = 0; i < files.length; i++) {
            droppable.querySelector('div').innerHTML += files[i].name + '<br>';
          }
          droppable.classList.add('filled');
        } else {
          droppable.querySelector('div').innerHTML = originalText;
          droppable.classList.remove('filled');
          droppable.querySelector('span').style.display = 'none';
        }
      };
      input.addEventListener('change', fileChanged);
      fileChanged(input);
      droppable.querySelector('span').addEventListener('click', function() {
        input.value = '';
        fileChanged(input);
      });
    });
  });
  