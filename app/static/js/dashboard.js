function MenuItem(menu_object) {
	var self = this;
	self.label = menu_object.label;
	self.icon = menu_object.icon;
	self.classes = menu_object.classes;
};

function PanelItem(panel_object) {
	var self = this;
	self.label = panel_object.label;
	self.url = panel_object.url;
};

function DashboardViewModel() {
	var self = this;
	self.allMenuItems = {
		list: {label: 'List', icon: 'fa fa-users fa-lg', classes: 'btn btn-lg btn-primary btn-block'},
		add: {label: 'Add', icon: 'fa fa-user-plus fa-lg', classes: 'btn btn-lg btn-info btn-block'},
		edit: {label: 'Edit', icon: 'fa fa-pencil-square fa-lg', classes: 'btn btn-lg btn-warning btn-block'}
	}
	self.allPanelItems = {
		overview: {label: 'Overview', url: "{{ url_for('user.dashboard', user=user) }}"},
		relationship: {label: 'Relationships', url: "{{ url_for('user.relationships', user=user) }}"},
		visualisation: {label: 'Visualisation', url: "#"},
		share: {label: 'Share', url: "#"}
	}
	self.chosenRelationshipMenuId = ko.observable();
	self.chosenDashboardPanelId = ko.observable();

	// Data
	self.relationshipMenus = [
		new MenuItem(self.allMenuItems.list),
		new MenuItem(self.allMenuItems.add),
		new MenuItem(self.allMenuItems.edit)
	];

	self.dashboardPanels = [
		new PanelItem(self.allPanelItems.overview),
		new PanelItem(self.allPanelItems.relationship),
		new PanelItem(self.allPanelItems.visualisation),
		new PanelItem(self.allPanelItems.share)
	];

	// Behaviours
	self.goToMenu = function(menu_item) {
		self.chosenRelationshipMenuId(menu_item.label)
	};

	self.goToPanel = function(panel) {
		self.chosenDashboardPanelId(panel.label)
	};

};

ko.applyBindings(new DashboardViewModel());