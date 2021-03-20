
function get_request(attr) {
    /** Get request for such id */

    var id_str = attr + '_id1';
    var info_id = document.getElementById(id_str).value
    var result = "---------------- </br>";

    var url = 'http://127.0.0.1:5000/' + attr + '?id=' + info_id;
   axios.get(url).then( 
       (response) => { 
           var res = response.data;
           for (item in res[0]) {
               if (item == '_id') {
                   continue;
               }
               result += item + " :" + res[0][item] + "</br>";
           }
        document.getElementById('info1').innerHTML = result;
        console.log("Successfully get " + attr + "info"); 

       }).catch(error => {
            document.getElementById('info1').innerHTML = 
                "No such id in database. Please enter a valid " + attr + "_id";
            console.log("Not valid id");
        }
    );
}


function delete_request(attr) {
    /** Delete request for such id */
    
    var id_str = attr + '_id2';
    var info_id = document.getElementById(id_str).value
    var url = 'http://127.0.0.1:5000/' + attr + '?id=' + info_id;
    axios.delete(url).then( 
        (response) => { 
            document.getElementById('info2').innerHTML = 
                "Successfully deleted " + attr + " with id: " + info_id;
            console.log("Successfully deleted");

        }).catch(error => {
            document.getElementById('info2').innerHTML = 
                "No such id in database. Please enter a valid " + attr + "_id";
            console.log("Not valid id");
        }
    );
}

function put_request(category) {
    /** Put request for such id */

    var id_str = category + '_id3';
    var info_id = document.getElementById(id_str).value
    var attr_str = category + '_attr3';
    var attribute = document.getElementById(attr_str).value;
    var val_str = category + '_val3';
    var value = document.getElementById(val_str).value;
    var url = 'http://127.0.0.1:5000/' + category + '?id=' + info_id;
    var new_dict = {};
    if (attribute == "rating") {
        new_dict[attribute] = parseFloat(value);
    } else if (attribute == "review_count" || (attribute == "rating_count")) {
        new_dict[attribute] = parseInt(value);
    } else {
        new_dict[attribute] = value;
    }
    axios.put(url, new_dict).then( 
        (response) => { 
            document.getElementById('info3').innerHTML = 
                "Successfully updated the " + attribute + " of the " + category;
            console.log("Successfully updated");

        }).catch(error => {
            document.getElementById('info3').innerHTML = 
                "No such id in database. Please enter a valid " + category + "_id";
            console.log("Not valid id");
        }
    );
}


function post_request() {
    /** Post request for such id */

    var category = document.getElementById('category_post').value
    var info_id = document.getElementById('id_post').value
    var name = document.getElementById('name_post').value;
    var url_post = document.getElementById('url_post').value;
    var rating = document.getElementById('rating_post').value;
    var rating_count = document.getElementById('rating_ct_post').value;
    var review_count = document.getElementById('review_ct_post').value;
    var url = 'http://127.0.0.1:5000/' + category;
    var new_dict = {};
    if (category == 'book') {
        new_dict['book_url'] = url_post;
        new_dict['title'] = name;
        new_dict['book_id'] = info_id;
    } else if (category == 'author') {
        new_dict['name'] = name;
        new_dict['author_url'] = url_post;
        new_dict['author_id'] = info_id;
    }
    new_dict['rating'] = parseFloat(rating);
    new_dict['rating_count'] = parseInt(rating_count);
    new_dict['review_count'] = parseInt(review_count);
    axios.post(url, [new_dict]).then( 
        (response) => { 
            document.getElementById('info4').innerHTML = 
                "Successfully insert the "+ category;
            console.log("Successfully updated");

        }).catch(error => {
            document.getElementById('info4').innerHTML = 
                "Failed to insert the " + category + ". Please try again";
            console.log("Failed to insert");
        }
    );
}