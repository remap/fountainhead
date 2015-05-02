# Contributing / Customizing

## Add web components

### How they are included

In parent HTML documents, such code

<pre>
\<link rel="import" href="components/example.html"\> 
...
\<com-example param1=val1></com-example\>
...
</pre>

will import a given web component file from given directory, and insert the component at given location.

An example of web component code looks like

<pre>
\<template>
    \<p></p>
\</template>

\<script>
    (function(window, document, undefined) {
        var MyElementProto = Object.create(HTMLElement.prototype);
        MyElementProto.str = "";
        
        MyElementProto.createdCallback = function() {
            ...
        };
        
        window.MyElement = document.registerElement('com-example', {
            prototype: MyElementProto
        });
    })(window, document);
\</script>
</pre>

Upon HTML _import_, the function in the script will be executed with parent window and document as parameter. The example function will create an object from HTML element, and register a prototype of that object on the parent window with a given name by calling parent window's _registerElement_. (Please note that web component names should follow a convention, see reference below.)

If your browser support web components, upon _insertion_ of the HTML element with your registered name, the _createdCallback_ in the sample code will be called. In the createdCallback, usually we would make a copy of the template in the web component html page under the created ShadowRoot, and operate on the elements in that template.

References:

* [Hello world web element](https://github.com/webcomponents/hello-world-element/blob/master/src/hello-world.html)
* [Web component templates](http://webcomponents.org/articles/introduction-to-template-element/)
* [Web component importing](http://www.html5rocks.com/en/tutorials/webcomponents/imports/)
* [Web component naming conventions](http://webcomponents.org/articles/how-should-i-name-my-element/)

### Existing helper prototypes

Many of our web components may share similar purposes. To avoid (over) duplicate of code, objects of two prototypes can be created in the web component to access their functions.

These prototypes are currently included once in the parent HTML document.

**ComponentObject**

Component object contains common functions such as applying styles of CSS classes from parent. They are created with:

<pre>
element.componentObject = new parentWindow.ComponentObject(parentWindow, window);
</pre>

And by calling

<pre>
element.componentObject.applyStyleFromParentDocument(childElement);
</pre>

The CSS style classes that you've assigned to childElement will try to inherit from the parent window's CSS. (Alternatively, you can include the parent's CSS file in the web component, though that would assume knowledge of the location of the CSS file.)

**NDNPublisherComponentObject**

Many of our components publish NDN data. This prototype contains functions for parsing NDN related parameters, and publishing NDN content under given name.

This sample code

<pre>
element.ndnPublisherComponentObject = new window.NDNPublisherComponentObject(this, window);
element.ndnPublisherComponentObject.parseParameters();
element.ndnPublisherComponentObject.publishContent(dataName, content, false);
</pre>

creates such a object, tries to parse the parameters passed to this element, and publishes NDN data.

_More prototype functions are being generalized._

### Examples

* [Random text component](https://github.com/remap/fountainhead/blob/master/html-test/components/random-text.html): creates a paragraph of random strings which changes periodically.

See it working [here](http://the-archive.la/script/fountainhead/html-test/test-component.html)

* [Online feed component](https://github.com/remap/fountainhead/blob/master/html-test/components/olf.html): creates a paragraph to follow the olf style class defined in parent document; and show/hide based on clicking in the parent window

* [NDN cue publishing component](https://github.com/remap/fountainhead/blob/master/html-test/components/cue-publisher.html): creates a title and a link; when clicking publishes NDN content, and when hovering, try to display youtube preview image.

* [The guide chat message sending component](https://github.com/remap/fountainhead/blob/master/html-test/components/chat-control-guide.html): creates a character and a dialogue, when clicking sends a chat message as the guide; works with dual dialogue styling as instructed from parent document.

## Add parser rules (Experimental)

Derive from fountain_regex class, fill in your additional regex, add HTML generation function and pass it as generateHtml as in FountainHTMLGenerator.