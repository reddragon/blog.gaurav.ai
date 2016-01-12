---
layout: post
title: "Writing a LISP interpreter in Go for an iOS app"
date: 2016-01-10 21:38:02 -0800
comments: true
categories:
---
In the summer of 2015, I wanted to work on a side-project that I can quickly use, instead of spending lots of weekends, and it getting no where. Luckily I found the right project on <a href="http://norvig.com/lispy.html" target="_blank">Peter Norvig's website</a>. Here I would try to describe in two parts, how to write a simple LISP interpreter, and how to put that in your iOS app.

To those who are new to LISP, its pretty simple to explain. LISP programs are based on something called '<a href="https://en.wikipedia.org/wiki/S-expression" target="_blank">s-expressions</a>'. It looks something like this:
$(operator$ $operand_1$ $operand\_2$ $operand\_3$ $...)$. Now, the operands can themselves be recursively computed too.

For example, this is a valid expression: $(\+$ $1$ $(\*$ $2$ $3))$. First we evaluate the inner $(\*$ $2$ $3)$ part, then the original expression resolves to $(\+$ $1$ $6)$, which then evaluates to $7$. This can go on recursively.

For a person designing an interpreter, LISP is the ideal real-life language to start with. This is for two reasons:

1. There are minimal symbols to interpret. '(' and ')' and the operators that you define.
2. The parsing is straight-forward and recursive. <a href="https://en.wikipedia.org/wiki/Syntactic_sugar" target="_blank">Zero syntactic-sugar</a>.

It is because you can have as small a subset of LISP that you want, that I could stay motivated and bring this project to closure.

## Lexing
Lexing involves finding _lexemes_, or syntactical tokens, which can then be interpreted. In the expression $(\+$ $1$ $2)$, the tokens are [$($, $+$, $1$, $2$,  $)$]. Sophisticated compilers use <a href="http://dinosaur.compilertools.net/" target="_blank">lex</a> or <a href="https://en.wikipedia.org/wiki/Flex_(lexical_analyser_generator)" target="_blank">flex</a> for finding these tokens, handling white-space, attaching the token type to these tokens, etc.

I did not want to bloat up my simple interpreter by using lex / flex. I found this nifty one-line bare-bones Lexer on Peter Norvig's article:

{% codeblock lex.py %}
def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
{% endcodeblock %}

Essentially, what this does is to handle white-space (somewhat). It basically adds spaces around the brackets, and then splits the expression on white-space. This doesn't work when other operators aren't separated by space properly, like $($$\+1$ $2)$ would be converted to $($ $\+1$ $2$ $)$. '$\+1$' would be considered one token.  

We need to do the replacement for all operators, but otherwise it works well, because LISP is simple enough that attaching types to tokens (and erroring out, if required) can be done at the time of parsing. The recurrent theme in the design of the interpreter, is to be lazy and push the harder problems to the next layer.

{% codeblock foo.go %}
Add non-embarassing code.
{% endcodeblock %}

## Constructing an AST
An Abstract Syntax Tree (or AST), will create a tree, where the leaf nodes are atomic values, and all the non-leaf nodes are operators. For example, for the expression, $(\+$ $1$ $(\*$ $2$ $3))$ it would look something like this:


First we would represent a node of this tree in the code, like this:
{% codeblock astNode.go %}
type ASTNode struct {
  children []*ASTNode // Children of this AST Node.
  isValue  bool       // Checks if this is a value (also if children == nil).  
  value    string
}
{% endcodeblock %}

Now we would make sure that the expression follows a structure, typically defined as a Grammar. And this process is called parsing. We however break down this into two parts:

1. Making sure only the s-expression is well formed. Basically, if the brackets are in the right order.
2. In the spirit of lazy programming, pushing the task of validating if the operators have the right operands to the next stage.

This means that given an expression like $(\+$ $1)$, this stage would only do step 1, and mark this expression to be okay, even though we know that $+$ needs two operands.
{% codeblock ast.go %}
// This method gets a list of tokens, and returns:
// 1. The ASTNode of the tree so formed.
// 2. Unused tokens in the end of the array.
// 3. Any error while constructing the tree.
// Removed some error handling to make it a little brief.
func getASTOfTokens(tokens []string) (*ASTNode, []string, error) {
  var token = ""
  tokensLen := len(tokens)
  // If it is an empty list of tokens, the AST is a nil node
  if tokensLen == 1 {
    token, tokens = pop(tokens)
    if !isValue(token) {
      return nil, tokens, errStr("value", token)
    }

    // Create a one-node AST.
    node := new(ASTNode)
    node.isValue = true
    node.value = token
    node.children = nil
    return node, tokens, nil
  } else {
    token, tokens = pop(tokens)
    // Expect an opening bracket to start.
    if token != openBracket {
      return nil, tokens, errStr(openBracket, token)
    }

    node := new(ASTNode)
    node.isValue = false
    // Create a slice with 0 length initially.
    node.children = make([]*ASTNode, 0)

    tokensLen = len(tokens)
    for len(tokens) != 0 && tokens[0] != closedBracket {
      var childNode *ASTNode = nil
      var err error = nil
      // If we get an opening brace, it means we need to recursively get the
      // AST of the sub-expression from here on.
      if tokens[0] != openBracket {
        token, tokens = pop(tokens)
        childNode, _, err = getASTOfTokens([]string{token})
      } else {
        childNode, tokens, err = getASTOfTokens(tokens)
      }

      if err != nil {
        return nil, tokens, err
      }
      node.children = append(node.children, childNode)
    }

    // Expect a closing bracket when ending.
    token, tokens = pop(tokens)
    if token != closedBracket {
      return nil, tokens, errStr(token, closedBracket)
    }
    return node, tokens, nil
  }
}
{% endcodeblock %}

You can see how the grammar for interpreting the s-expression grammar is hard-coded here. We expect either a single value, or an something like $($$operator$ $o\_1$ $o\_2$ $...$ $)$, where $o\_i$ can be an atomic value, or a nested expression. They are all `ASTNode` objects, and are returned as part of the `children` slice.

## Parsing & Evaluation
We combine the parsing and evaluation of the AST into one stage. The result of evaluating an AST is an `Atom`, which can either have a `Value` or an `errror`.
{% codeblock atom.go %}
// An Atom is either a value, or an error
type Atom struct {
  Err error
  Val Value
}
{% endcodeblock %}

This is a stripped down AST evaluation code here.
{% codeblock eval.go %}
func evalAST(env *LangEnv, node *ASTNode) Atom {
  var retVal Atom
  if node.isValue {
    retVal.Value, retVal.Err = getValue(env, node.value)
    return retVal
  }

  // Assuming that the first child is an operand
  symbol := node.children[0].value
  operator := env.getOperator(symbol)

  // Skipped error handling related to operator & arguments for brevity.
  operands := make([]Atom, 0)
  for i := 1; i < len(node.children); i++ {
    v := evalAST(env, node.children[i])
    if v.Err != nil {
      return v
    }
    operands = append(operands, v)
  }

  v := operator.handler(env, operands)
  if v.Err != nil {
    return v
  }
  retVal.Val = v.Val
  return retVal
}
{% endcodeblock %}
Basic evaluation is very simple. We have an environment type called `LangEnv`, where we can register operators. When evaluating an AST, if its a single node, the value of the node is the result. Otherwise, we simply lookup the operator in the environment using `getOperator`, resolve the operands recursively, and pass the operands to the operator. The operand deals with making sure that the operands are sane.

An operator looks something like this:
{% codeblock operator.go %}
type Operator struct {
  symbol           string
  minArgCount      int
  maxArgCount      int
  handler          (func(*LangEnv, []Atom) Atom)
}
{% endcodeblock %}
As seen, `symbol` is the name of operator, so for the binary addition it can be "+". `handler` is the function which will actually do the heavy lifting we have been avoiding all this while. It takes in a slice of `Atom`s (and a `LangEnv`, more on that later) and returns an `Atom` as a result.

Now, the fun stuff.

## Type System
Remember `Atom` has a `Value` inside? `Value` is an interface, and any type which wants to be a `Value`, needs to implement the following methods.

{% codeblock value.go %}
type Value interface {
  Str() string                 // Returns a string representation of the value.
  getValueType() valueType     // Return the valueType (enum of all Values).
  to(valueType) (Value, error) // Convert to a different Value type.  
  ofType(string) bool          // Check if a given string is of this type.
  newValue(string) Value       // Create a new Value of this type.
}
{% endcodeblock %}

This is enough power to figure out which value is of which type. In `LangEnv` we keep a list of builtin `Value` types, such as `intValue`, `floatValue`, `stringValue`, etc.

To deduce the type of a value, we simply do this:

{% codeblock getValue.go %}
func getValue(env *LangEnv, token string) (Value, error) {
  types := builtinTypes()
  for _, t := range types {
    if t.ofType(token) {
      return t.newValue(token), nil
    }
  }
  return nil, errors.New(fmt.Sprintf("Could not get type for token: %s", token))
}
{% endcodeblock %}

Now imagine an expression like $(\+$ $1.2$ $3)$.

$1.2$ resolves to `floatValue`, and $3$ resolves to `intValue`. How would we implement the `handler` method for the $+$ operator to add these two different types? You might say, that this would involve _casting_ of $3$ to `floatValue`. Now how do we decide what values to cast, and what type should we cast them to?

This is how we do it. In the method, `typeCoerce`, we try to find out which is the right value type to cast all our values to. It is declared like:
`func typeCoerce(operatorName string, operands *[]Atom, typePrecendenceMap map[valueType]int) (valueType, error)`

This is what we do inside `typeCoerce`:

1. We get the type -> count mapping.
2. If there is only one type, there is nothing to do, return the corresponding type.
3. If there are multiple types, pick the one with the highest precedence.
4. Try and cast all operand values to that type. Error out if any of them resists. Because, resistance is futile.

Hence, the $+$ operator would be implemented something like this:
{% codeblock operator.go %}
addOperator(opMap,
  &Operator{
    symbol:      add,
    minArgCount: 2,
    maxArgCount: 100,
    handler: func(env *LangEnv, operands []Atom) Atom {
      var retVal Atom
      var finalType valueType
      finalType, retVal.Err = chainedTypeCoerce(add, &operands, []map[valueType]int{numValPrecedenceMap, strValPrecedenceMap})
      if retVal.Err != nil {
        return retVal
      }

      switch finalType {
      case intType:
        var finalVal intValue
        finalVal.value = 0
        for _, o := range operands {
          v, ok := o.Val.(intValue)
          if ok {
            finalVal.value = finalVal.value + v.value
          } else {
            fmt.Errorf("Error while converting %s to intValue\n", o.Val.Str())
          }
        }
        retVal.Val = finalVal
        break

      case floatType:
        var finalVal floatValue
        finalVal.value = 0
        for _, o := range operands {
          v, ok := o.Val.(floatValue)
          if ok {
            finalVal.value = finalVal.value + v.value
          } else {
            fmt.Errorf("Error while converting %s to floatValue\n", o.Val.Str())
          }
        }
        retVal.Val = finalVal
        break

        retVal.Val = finalVal.newValue(fmt.Sprintf("\"%s\"", buffer.String()))
        break
      }
      return retVal
    },
  },
)
{% endcodeblock %}

## Defining Variables

## Defining Methods

## Recursion
