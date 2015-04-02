# Fountain+ Syntax

Description of added Fountain+ syntax used by current parser (tag name REMAP).

For basic fountain syntax, please refer to [this page](http://fountain.io/syntax).

## Web component declaration

Web component declarations include web components in component parent folder, and insert them into the parsed html.

* **Syntax**: 
<pre>
<<@componentA[(arg1=val1,arg2=val2...)] text-description>>
</pre>
* **HTML output**: 
<pre>
\<link rel="import" href="components/componentA.html"\> 
\<!-- once per file --\> \<componentA arg1="val1" arg2="val2">text description</component\>
</pre>
* **Description**: Web components only appear in Action; The components parent folder can be specified with parser parameters.

## Preamble section declaration

### Environment declaration

Environment declarations declare Javascript variables for usage in the parsed html or web components;

* **Syntax**: 
<pre>
# Environment 
[variable1] javascript code
... 
# ...
</pre>
* **HTML output**: 
<pre>
\<script\>var name1 = javascript code;...\</script\>
</pre>
* **Description**: A few keywords, such as 'include' are retained for special purposes

  #### Specially handled environments:

  ###### Include

  Includes insert Javascript code from specified files into the parsed html.

  * **Syntax**: 
  <pre>
  [include1] filename
  </pre>
  * **HTML output**: 
  <pre>
  \<script src="js/filename"\>\</script\>
  </pre>
  * **Description**: The includes parent folder can be specified with parser parameters

  ###### NDN-JS

  ###### Strophe-JS

**Pending**: should the following ones be generalized, or handled by plugins to the parser?
  
### Character type declaration

Character type declarations generate a table and apply corresponding CSS classes for character types description.

* **Syntax**: 
<pre>
# CharacterTypes 
[type1] description
... 
# ...
</pre>
* **HTML output**: 
<pre>
\<div id="charactertypecontent"\>
  \<table\>
    \<td\>
      \<p class=type1-def\>type1\</p\>
      \<p class=charactertypecontent-desc\>description\</p\>
    \</td\>
  \</table\>
\</div\>
</pre>
* **Description**: Characters in character declaration section will be associated with classes declared in this section.

### Character declaration

Character declarations declare characters, and associate them with CSS classes of the types that they belong to.

* **Syntax**: 
<pre>
# Characters 
name1 [type1] description
... 
# ...
</pre>
* **HTML output**:
<pre>
\<div id="charactercontent"\>
  \<p class='name1-def'\>name1\</p\>
  \<p class='charactercontent-desc'\>description\</p\>
\</div\>
</pre>
* **Description**: By correlating a character name here with a character type, all the dialogues of this character will be assigned corresponding class for the character's type

### Setting declaration

Setting declarations describe other settings that want to get rendered in the html.

* **Syntax**: 
<pre>
# Settings 
[name1] description
... 
# ...
</pre>
* **HTML output**:
<pre>
\<div id="settingcontent"\>
  \<p class='name1-def'\>name1\</p\>
  \<p class='settingcontent-desc'\>description\</p\>
\</div\>
</pre>
* **Description**: Settings declarations has the same syntax as character type declarations

### Body declaration

Body declaration declares the beginning of the actual script.

* **Syntax**: 
<pre>
# Body 
...
</pre>
* **HTML output**:
<pre>
\<div id="scriptbody"\>
    ...
\</div\>
</pre>
* **Description**: Body declaration should be the last of the preamble sections; and all content after this section will be parsed with fountain syntax and web component syntax