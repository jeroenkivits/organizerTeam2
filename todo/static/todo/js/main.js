var ListPage = {
	init: function() {
		this.$container = $('.lists-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

var ItemPage = {
	init: function() {
		this.$container = $('.items-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

var FavoritPage = {
	init: function() {
		this.$container = $('.favorites-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();
			window.location.reload(true);
			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

var CheckedPage = {

	init: function() {
		this.$container = $('.checked-container');
		this.render();
		this.bindEvents()
	},

	render: function() {
	},

	bindEvents: function() {
		$('.btn-checked', this.$container).on('click', function(e) {
			e.preventDefault();
			link = window.location.href
			if (link.includes("add")){
				link = link.split("add")[0];
			} else {
				link = link.split("delete")[0];
			}
			window.location.replace(link);
			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-unchecked', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

var CheckedListPage = {

	init: function() {
		this.$container = $('.listscheck-container');
		this.render();
		this.bindEvents()
	},

	render: function() {
	},

	bindEvents: function() {
		$('.btn-checked', this.$container).on('click', function(e) {
			e.preventDefault();
			window.location.reload(true);
			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-unchecked', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};


$(document).ready(function() {
	ListPage.init();
	FavoritPage.init();
	ItemPage.init();
	CheckedPage.init();
	CheckedListPage.init();
});
