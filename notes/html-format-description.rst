Notebook HTML format
====================

Each line of code is wrapped in  a pre tag.
Individual tokens are wrapped in span tags for highlighting purposes.
The ``cm-`` stands for `CodeMirror <http://codemirror.net/>`__ ,
the editor that IPyNB uses.

For example:

::

    <pre>
      <span class="cm-builtin">
        len
      </span>
      ([[
      <span class="cm-variable">
        i
      </span>
      ,
      <span class="cm-variable">
        i
      </span>
      <span class="cm-operator">
        *
      </span>
      <span class="cm-number">
        2
      </span>
      ]
      <span class="cm-keyword">
        for
      </span>
      <span class="cm-variable">
        i
      </span>
      <span class="cm-operator">
        in
      </span>
      <span class="cm-variable">
        x
      </span>
      ])
    </pre>



This code shows the first cell in a notebook.
It includes a

* Input prompt (In \[5\])
* an ``input_area``, in this case filled with a ``CodeMirror`` div.
* an ``output_area``, in this case filled with the line of output "Populating the interactive namespace from numpy and matplotlib"

::
 
    <div class="cell border-box-sizing code_cell" tabindex="2">
    <div class="input">
      <div class="prompt input_prompt">
      In&nbsp;[5]:
      </div>
      <div class="vbox box-flex1">
      <div class="ctb_hideshow">
        <div class="celltoolbar hbox reverse">
        </div>
      </div>
      <div class="input_area">
        <div class="CodeMirror cm-s-ipython">
        <div style="overflow: hidden; position: relative; width: 3px; height: 0px; top: 5.71875px; left: 5.71875px;">
          <textarea autocorrect="off" autocapitalize="off" spellcheck="false" tabindex="0" style="position: absolute; padding: 0px; width: 1000px; height: 1em; outline: none; font-size: 4px;">
          </textarea>
        </div>
        <div class="CodeMirror-hscrollbar" style="left: 0px;">
          <div style="height: 1px;">
          </div>
        </div>
        <div class="CodeMirror-vscrollbar">
          <div style="width: 1px;">
          </div>
        </div>
        <div class="CodeMirror-scrollbar-filler">
        </div>
        <div class="CodeMirror-gutter-filler">
        </div>
        <div class="CodeMirror-scroll" tabindex="-1">
          <div class="CodeMirror-sizer" style="min-width: 137px; margin-left: 0px; min-height: 28px;">
          <div style="position: relative; top: 0px;">
            <div class="CodeMirror-lines">
            <div style="position: relative; outline: none;">
              <div class="CodeMirror-measure">
              <pre>
                <span class="cm-operator">
                %
                </span>
                <span class="cm-variable">
                p
                </span>
                <span class="cm-variable">
                y
                </span>
                <span class="cm-variable">
                l
                </span>
                <span class="cm-variable">
                a
                </span>
                <span class="cm-variable">
                b
                </span>
                <span>
                </span>
                <span class="cm-variable">
                i
                </span>
                <span class="cm-variable">
                n
                </span>
                <span class="cm-variable">
                l
                </span>
                <span class="cm-variable">
                i
                </span>
                <span class="cm-variable">
                n
                </span>
                <span class="cm-variable">
                e
                </span>
              </pre>
              </div>
              <div style="position: relative; z-index: 1; display: none;">
              </div>
              <div class="CodeMirror-code" style="">
              <pre>
                <span class="cm-operator">
                %
                </span>
                <span class="cm-variable">
                pylab
                </span>
                <span class="cm-variable">
                inline
                </span>
              </pre>
              </div>
              <div class="CodeMirror-cursor" style="left: 0px; top: 0px; height: 17px;">
              &nbsp;
              </div>
              <div class="CodeMirror-cursor CodeMirror-secondarycursor" style="display: none;">
              &nbsp;
              </div>
            </div>
            </div>
          </div>
          </div>
          <div style="position: absolute; height: 30px; width: 1px; top: 28px;">
          </div>
          <div class="CodeMirror-gutters" style="display: none; height: 28px;">
          </div>
        </div>
        </div>
      </div>
      </div>
    </div>
    <div class="output_wrapper">
      <div class="out_prompt_overlay prompt" title="click to expand output; double click to hide output" style="">
      </div>
      <div class="output vbox" style="">
      <div class="output_area">
        <div class="prompt">
        </div>
        <div class="output_subarea output_text output_stream output_stdout">
        <pre>
          Populating the interactive namespace from numpy and matplotlib
        </pre>
        </div>
      </div>
      </div>
      <div class="btn output_collapsed" title="click to expand output" style="display: none;">
      . . .
      </div>
    </div>
    </div>



This code shows the In[Num] that's repeated for each cell in the notebook 

:: 

    <div class="input">
    <div class="prompt input_prompt">
      In&nbsp;[7]:
    </div>
    <div class="vbox box-flex1">
      <div class="ctb_hideshow">
      <div class="celltoolbar hbox reverse">
      </div>
      </div>
      <div class="input_area">
      <!-- This is where the Python CodeMirror stuff goes. -->
      </div>
    </div>
    </div>



This code shows the output of ploting some data ( this part is kind of long because it outputs a line of text 
and a graph:

1. the line of text 

::

    <div class="output_area">
    <div class="prompt output_prompt">
      Out[16]:
    </div>
    <div class="output_subarea output_text">
      <pre>
      [&lt;matplotlib.lines.Line2D at 0xf3c10f0&gt;]
      </pre>
    </div>
    </div>


2. the code for the graph 

Where it says ``[SNIP]`` there is typically much more data.

::

    <div class="output_area">
    <div class="prompt">
    </div>
    <div class="output_subarea output_png">
      <div class="ui-wrapper" style="overflow: hidden; position: relative; width: 376px; height: 256px; top: auto; left: auto; margin: 0px;">
      <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXgAAAEACAYAAAC57G0KAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz
        AAALEgAACxIB0t1+/AAAIABJREFUeJztfX10HMWd7R1pZEn+lizbYEnE2BLYxmCbNRhCyIoQx5iD
        TRbYxGSXZIkP6wBe8sXZ7Elesji7sTGbfQkb79vnLIRAsjF+5OWtIYfoECAKSQw4YAMJNkY4Fkjy
        [SNIP]
        " class="ui-resizable" style="margin: 0px; resize: none; position: static; zoom: 1; display: block; height: 256px; width: 376px;" />
      <div class="ui-resizable-handle ui-resizable-e" style="z-index: 90; display: block;">
      </div>
      <div class="ui-resizable-handle ui-resizable-s" style="z-index: 90; display: block;">
      </div>
      <div class="ui-resizable-handle ui-resizable-se ui-icon ui-icon-gripsmall-diagonal-se" style="z-index: 90; display: block;">
      </div>
      </div>
    </div>
    </div>

