function LoadSubList(){
    document.querySelector('#cloud_compting').innerHTML = "\
    <p style='cursot: pointer'>Cloud Computing</p>\
    <div style='text-align: left; padding-left:5px;' class = 'subList'>\
    <p style='cursor: pointer' onclick='LoadBoard()'> └ 2020-SPRING-MID</p>\
    <p style='cursor: pointer'> └ 2020-FALL-MID</p>\
    <p style='cursor: pointer'> └ 2021-SPRING-MID</p>\
    </div>"



    // document.write("<div style='text-align: left; padding-left:5px;' class = 'subList'>")
    // document.write("<p style='cursor: pointer'> └ 2020-SPRING-MID</p>")
    // document.write("<p style='cursor: pointer'> └ 2020-FALL-MID</p>")
    // document.write("<p style='cursor: pointer'> └ 2021-SPRING-MID</p>")
    // document.write("</div>")
}

function LoadBoard(){

    document.querySelector('.board').innerHTML = "\
    <h2 style='padding-left: 120px'>Board</h2>\
    <ul style='list-style: none; padding: 10px 20px 20px 120px;'>\
    <li><a href=\"blank\">1-3 문제 질문드려요.</a></li>\
    <li><a href=\"blank\">S3 cost model 최적화</a></li>\
    <li><a href=\"blank\">On-demand requirements</a></li>\
    <li><a href=\"blank\">Reserved requirements</a></li>\
    <li><a href=\"blank\">Spot requirements</a></li>\
    "
    // document.write("<h2 style='padding-left: 120px'>Board</h2>");
    // document.write("<ul style='list-style: none; padding: 10px 20px 20px 120px;'>");
    // document.write('<li><a href="blank">1-3 문제 질문드려요.</a></li>');
    // document.write('<li><a href="blank">S3 cost model 최적화</a></li>');
    // document.write('<li><a href="blank">On-demand requirements</a></li>');
    // document.write('<li><a href="blank">Reserved requirements</a></li>');
    // document.write('<li><a href="blank">Spot requirements</a></li>');
    // document.write("</ul>");
}