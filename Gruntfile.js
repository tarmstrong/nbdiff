module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    qunit: {
      files: ['src/test/index.html']
    },
    jshint: {
      all: ['Gruntfile.js', 'src/test/*.js', 'src/*']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('test', ['qunit']);
  // Travis CI task.
  grunt.registerTask('travis', ['jshint', 'qunit']);

  grunt.registerTask('default', ['qunit', 'jshint']);

};
