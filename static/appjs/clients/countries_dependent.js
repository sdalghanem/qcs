//هذه صفحة الاستعلامات 
// page - > clients/queries.html
// عرض الدول و المدن و الفروع 

// توضع في كل صفحة تحتاج فيها دروب داون لست 
// دروب داون لست للمدن
let region = document.getElementById("region")
let city = document.getElementById("city")
let district = document.getElementById("district")
let branch = document.getElementById("branch")
let brand = document.getElementById("brand")  

region.addEventListener('change', function() {
        if(region.value != 0)  {
            city.style.display = 'inline'; // Show the city dropdown
            city.innerHTML = " ";
            city.innerHTML = "<option value='0'>الكل</option> ";
            console.log(region.value)
///////////////////////////////////////////////////////////////
            $.ajax({
            type: 'post',
            url:'/clients/cities_list',
            async: true,
            data:{
            regionID   : region.value,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        } ,
        
            success:function(data){ 
             data.forEach((element) => {
                city.innerHTML += `
                <option value="${element.id}">${element.name}</option>
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
            city.style.display = 'none';
            district.style.display = 'none';
            branch.style.display = 'none';

        }
        
    });


// دروب داون لست المدن عند الاختيار تطلع الاحياء وعند اختيار الكل تختفي الاحياء
city.addEventListener('change', function() {
    if(city.value != 0)  {
        district.style.display = 'inline'; // Show the city dropdown
        district.innerHTML = " ";
        district.innerHTML = "<option value='0'>الكل</option> ";
        console.log(city.value)
///////////////////////////////////////////////////////////////
        $.ajax({
        type: 'post',
        url:'/clients/district_list',
        async: true,
        data:{
        cityID   : city.value,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    } ,
    
        success:function(data){ 
         data.forEach((element) => {
            district.innerHTML += `
            <option value="${element.id}">${element.name}</option>
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
        district.style.display = 'none';
        branch.style.display = 'none';

    }
});


// دروب داون لست الاحياء عند الاختيار تطلع الفروع وعند اختيار الكل تختفي الفروع
district.addEventListener('change', function() {
    if(district.value != 0)  {
        //alert(brand.value)
        branch.style.display = 'inline'; // Show the city dropdown
        branch.innerHTML = " ";
        branch.innerHTML = "<option value='0'>الكل</option> ";
        console.log(district.value)
///////////////////////////////////////////////////////////////
        $.ajax({
        type: 'post',
        url:'/clients/branch_list',
        async: true,
        data:{
        districtID   : district.value,
        brand_id : brand.value,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    } ,
    
        success:function(data){ 
         data.forEach((element) => {
            branch.innerHTML += `
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
        branch.style.display = 'none';
    }
});




/////////////////////////departments//////////////////////////
