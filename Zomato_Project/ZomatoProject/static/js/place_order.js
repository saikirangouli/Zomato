var selected_restaurant = document.getElementsByClassName('update-cart')
for(let i=0;i<selected_restaurant.length;i++)
{
    selected_restaurant[i].addEventListener('click',function(){
        var restaurant_id = this.dataset.product
        var action=this.dataset.action
        console.log('Restaurant_id,',restaurant_id)
        console.log(action)

    })
}
