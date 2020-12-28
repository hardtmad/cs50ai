# Language - Parser 
Using a Context-Free Grammar (CFG), the AI parses natural English sentences into syntactic categories, such as Noun Phrase (NP). The CFG contains terminal rules, which are elementary symbols or leaf nodes of the grammar (ex: `N -> "holmes"`) and nonterminal rules, which are non-leaf nodes that produce the grammar (ex: `S -> NP VP`). Syntactic categories can be helpful in understanding the semantic meaning of a sentence. In particular, noun phrases can be used to identify to subject matter of a sentence.  

<pre>
Holmes chuckled to himself. 
                 S                 
   ______________|___                 
  |                  VP              
  |        __________|___              
  |       |              PP          
  |       |           ___|_____        
  NP      VP         |         NP     
  |       |          |         |       
  N       V          P         N   
  |       |          |         |     
holmes chuckled      to     himself  
</pre>

# Datasets
* sentences/*.txt - sample sentences 1-10 using corpus words 

# Running
python parser.py [sentence]

# Demonstration
https://youtu.be/C52TIQsdKtA
