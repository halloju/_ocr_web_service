// import $ from 'jquery/dist/jquery'
import jQuery from 'jquery';
Object.assign(window, { $: jQuery, jQuery })
//or
window.jQuery = window.$ = $