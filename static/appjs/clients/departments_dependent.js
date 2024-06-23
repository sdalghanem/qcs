let department = document.getElementById("department")
let section = document.getElementById("section")
let evalu = document.getElementById("evalu")

  

department.addEventListener('change', function() {
        if(department.value != 0)  {
            section.style.display = 'inline'; // Show the section dropdown
            evalu.style.display = 'inline'; // Show the evaluation dropdown
            section.innerHTML = " ";
            section.innerHTML = "<option value='0'>الكل</option> ";
           // console.log(department.value)
///////////////////////////////////////////////////////////////
            $.ajax({
            type: 'post',
            url:'/clients/sections_list',
            async: true,
            data:{
            department_id   : department.value,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        } ,
        
            success:function(data){ 
               // console.log(data)
             data.forEach((element) => {
                section.innerHTML += `
                <option value="${element.id}">${element.description}</option>
                `;
             });
            },
            done:function(data){
                console.log('done ->>' + data)
            },
            error:function(data){
                console.log('error ->>' + data);

            }
    });
//////////////////////////////////////////////////////////////////
        }
        else{
            section.style.display = 'none';
            evalu.style.display = 'none';


        }
        
    });
