module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    qunit: {
      files: ['jstests/index.html']
    },
    jshint: {
      all: [
        'Gruntfile.js',
        'jstests/*.js',
        'nbdiff/server/static/*.js'
      ],
      options: {
        jshintrc: '.jshintrc'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('test', ['qunit']);
  // Travis CI task.
  grunt.registerTask('travis', ['jshint', 'qunit']);

  grunt.registerTask('default', ['qunit', 'jshint']);

};
