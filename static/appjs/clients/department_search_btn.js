let fillter_btn = document.getElementById("fillter_btn");
let result_table = document.getElementById("result-table");
let model_responsible = document.getElementById("model_responsible");
let per = document.getElementById("per")
let img_model = document.getElementById("img_model")
let thead_custom = document.getElementById("thead_custom")
// زر الاستعلام
fillter_btn.addEventListener('click', function() {
    //
    get_percentage(report.value)
    report_view(report.value)
});

// ج
function report_view(x){
    result_table.innerHTML = " "
    thead_custom.innerHTML = " "
    thead_custom.innerHTML += `                          
                                    <th>البند</th>
                                    <th>التقييم</th>
                                    <th>الملاحظات</th>
                                    <th>المرفقات</th>
                                    <th>المسؤولين</th> 
                                `;
    $.ajax({
            type: 'post',
            url:'/clients/view_report',
            async: true,
            data:{
            orderid   : x ,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        } ,
        
            success:function(data){ 
               // console.log(data)
             data.forEach((element) => {
                if (element.score == 1){
                    score = 'نعم'
                    score_class = 'badge badge-light-success'
                } else if(element.score == 0){
                    score = 'لا'
                    score_class = 'badge badge-light-danger'
                } else{
                    score = 'مستبعد'
                    score_class = 'badge badge-light-primary'
                }
                result_table.innerHTML += `<tr>
                                                <td>${element.description}  </td>
                                                <td> <button class='${score_class}'>${score} </button></td>
                                                <td> ${element.note} </td>
                                                <td> ${element.img ? `<button class='btn badge badge-light-primary' data-bs-toggle='modal' data-bs-target='#imgsliderModal'  onclick="view_term_img('`+element.img+`')"> عرض</button>` : ''} </td>
                                                <td> <button class='btn badge badge-light-primary' data-bs-toggle="modal" data-bs-target="#sliderModal"  onclick="get_responisbles(${element.id})"> المسؤولين</button> </td>
                                            </tr>`
             });
            },
            done:function(data){
                console.log('done ->>' + data)
            },
            error:function(data){
                console.log('error ->>' + data);

            }
        });
}

// <td><button class='btn badge badge-light-primary' data-bs-toggle='modal' data-bs-target='#imgsliderModal'  onclick="view_term_img('${element.img}')"> عرض</button></td>

//<td>   ${ element.img.length != 0 ? "<button class='btn badge badge-light-primary' data-bs-toggle='modal' data-bs-target='#imgsliderModal'  onclick='view_term_img('"+ element.img +"')'> "+ typeof(element.img) +"</button>"  : '' }</td>


function get_percentage(x){
    per.innerHTML = '';
    $.ajax({
        type: 'post',
        url:'/clients/get_percentage',
        async: true,
        data:{
        orderid   : x,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    } ,
    
        success:function(data){ 
         
           return  per.innerHTML = `التقييم <br> <h1> ${data.percentage} %</h1>` 

         
        },
        done:function(data){
            console.log('done ->>' + data)
        },
        error:function(data){
            console.log('error ->>' + data);

        }
    });
}


function get_responisbles(x){
    //alert(x)
    model_responsible.innerHTML = ` `;
    $.ajax({
        type: 'post',
        url:'/clients/get_responisbles',
        async: true,
        data:{
        termid   : x ,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    } ,
    
        success:function(data){ 
           // console.log(data)
             data.forEach((element) => {
                //console.log(element)
                 model_responsible.innerHTML+= `<tr>
                                                <td> ${element.name} </td>
                                                <td> ${element.sections}</td>
                                                </tr>`;
             });

         
        },
        done:function(data){
            console.log('done ->>' + data)
        },
        error:function(data){
            console.log('error ->>' + data);

        }
    });
}





function view_term_img(x){
    console.log(x)
    img_model.innerHTML = ` `;
    img_model.innerHTML += `<img class="d-block w-100" src="../media/${x}" alt="Third slide"></img> `;
    
    
}
function view_term_img2(x){
    img_model2 = document.getElementById("img_model2")
    console.log(x)
    img_model2.innerHTML = ` `;
    img_model2.innerHTML += `<img class="d-block w-100" src="../../../${x}" alt="Third slide"></img> `;
    
    
}
