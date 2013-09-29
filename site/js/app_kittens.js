(function() {
    App = Ember.Application.create();

    App.Store = DS.Store.extend({
      revision: 12,
    });

    
    App.Kitten = DS.Model.extend({
        name: DS.attr('string'),
        picture: DS.attr('string'),
    });

    App.KittenAdapter = DS.RESTAdapter.extend({
        namespace: 'api'
    });

    App.IndexRoute = Ember.Route.extend({
        model: function() {
            return this.store.find('kitten');
        },

        actions: {
            deleteKitten: function(kitten) {
                kitten.deleteRecord();
                kitten.save();
            }
        }
    });

    // Add some routes
    App.Router.map(function() {
        this.route('create');
        this.route('edit', {path: '/edit/:kitten_id'});
    });

    // Add a controller to dispatch create commands
    App.CreateController = Ember.Controller.extend( {
        name: null,
        actions: {
            save:function() {
            var kitten =this.store.createRecord('kitten');
                kitten.set('name', this.get('name'));
                kitten.save().then(function() {
                    this.transitionToRoute('index');
                    this.set('name', '');
                }.bind(this));
            }
        }
    });
    App.EditController = Ember.ObjectController.extend({
        actions: {
            save: function() {
                var kitten = this.get('model');
                kitten.save().then(function() {
                    this.transitionToRoute('index');
                }.bind(this));
            }
        }
    });

})();
