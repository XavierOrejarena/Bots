var thirdPartyURL = 'https://api.github.com/repositories/11730342/commits?per_page=5&sha=';
// var thirdPartyURL = './Silkroad.json';

new Vue({

  el: '#liveApp',

  data: {
    currentBranch: 'dev',
    comments: null
  },

  created: function () {
    this.get_Data();
  },

  methods: {
    get_Data: function () {
    var self = this;
    $.get( thirdPartyURL, function( data ) {
        console.log(data);
        self.comments = data;
    });

    }

  }
});