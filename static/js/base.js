// //form add
// var title = $('#title')
// var authors_str = $('#authors_str')
// var tags_str = $('#tags_str')
// var pdf = $('#pdf')
// var modal_add_book = $('#modal_add_book')


// $(document).ready(function() {
// 	modal_add_book.on('submit', function(param){
// 		$.ajax({
// 			url: '/books/add/',
// 			type: 'POST',
// 			dataType: 'json',
// 			data: modal_add_book.serialize(),
// 		})
// 		.done(function(data) {
// 			console.log("success");
// 		})
// 		.fail(function(data) {
// 			console.log("error");
// 		})
// 		.always(function(data) {
// 			console.log(data);
// 		});
		
// 		return false;
// 	});
// });