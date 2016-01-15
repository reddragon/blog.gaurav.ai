---
layout: post
title: "[WIP] Writing a LISP interpreter in Go for an iOS app"
date: 2016-01-10 21:38:02 -0800
comments: true
categories:
---
In the summer of 2015, I wanted to work on a side-project that I can quickly use, instead of spending lots of weekends, and it getting no where. Luckily I found the right project on <a href="http://norvig.com/lispy.html" target="_blank">Peter Norvig's website</a>. Here I would try to describe in two parts, how to write a simple LISP interpreter, and how to put that in your iOS app.

To those who are new to LISP, its pretty simple to explain. LISP programs are based on something called '<a href="https://en.wikipedia.org/wiki/S-expression" target="_blank">s-expressions</a>'. It looks something like this:
$(operator$ $operand_1$ $operand\_2$ $operand\_3$ $...)$.

For example:

* $(+\ 1\ 2)$ in LISP is the same as $1\ +\ 2$.
* $(*\ 2\ 3\ 4)$ in LISP evaluates to $2\ *\ 3\ *\ 4$.

Now, the operands can themselves be recursively computed too.

For example, this is a valid expression: $(\+$ $1$ $(\*$ $2$ $3))$. First we evaluate the inner $(\*$ $2$ $3)$ part, then the original expression resolves to $(\+$ $1$ $6)$, which then evaluates to $7$. This can go on recursively.

For a person designing an interpreter, LISP is the ideal real-life language to start with. This is for two reasons:

1. There are minimal symbols to interpret. '(' and ')' and the operators that you define.
2. The parsing is straight-forward and recursive. Zero <a href="https://en.wikipedia.org/wiki/Syntactic_sugar" target="_blank">syntactic-sugar</a>.

It is because you can have as small a subset of LISP that you want, that I could stay motivated and bring this project to closure.

## What I Built
To keep you motivated about reading the article, lets do the demo first and then we can talk about how I built this.

[TODO: youtube video.]

Here is the <a href="https://github.com/reddragon/lambda" target="_blank">code for the interpreter</a>, and the <a href="https://itunes.apple.com/lc/app/lambda-lisp/id1046408504?mt=8" target="_blank">app on iTunes</a>. Feel free to file issues / contribute.

If you are still reading, let's build an interpreter!

## Lexing
Lexing involves finding _lexemes_, or syntactical tokens, which can then be combined to interpret a grammatical sentence. In the expression $(\+$ $1$ $2)$, the tokens are [$($, $+$, $1$, $2$,  $)$]. Sophisticated compilers use <a href="http://dinosaur.compilertools.net/" target="_blank">lex</a> or <a href="https://en.wikipedia.org/wiki/Flex_(lexical_analyser_generator)" target="_blank">flex</a> for finding these tokens, handling white-space, attaching a token type to each of them, etc.

I did not want to bloat up my simple interpreter by using lex / flex. I found this nifty one-line bare-bones Lexer in Peter Norvig's article:

{% codeblock lex.py %}
def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
{% endcodeblock %}

Essentially, what this does is to handle white-space (somewhat). It basically adds spaces around the brackets, and then splits the expression on white-space.

We need to do the replacement for all operators, but otherwise it works well, because LISP is simple enough that attaching types to tokens (and erroring out, if required) can be done at the time of parsing. This is how I did it in Go, just for completeness sake.

{% codeblock tokenizer.go %}
func tokenize(exp string) []string {
  return strings.Fields(
    strings.Replace(strings.Replace(exp, "(", " ( ", -1), ")", " ) ", -1),
  )
}
{% endcodeblock %}

The recurrent theme in the design of this interpreter, is to be lazy and push the harder problems to the next layer.

## Constructing an AST
Given an expression, we would need to make sure that the expression follows a structure, or a Grammar. This means two things in our case:

1. The s-expression should be well formed. The brackets should be balanced, should not be out of order, etc.
2. Operators such as $+$, $*$, etc. get the right number / type of operators, etc.

At this stage, we are only concerned about well-formedness of the s-expression. We don't care if the $+$ operator received incompatible operands, or any of these other problems. This means that given an expression like $(\+$ $1)$, we would mark this expression to be okay at this point, because the expression is well-formed. We will catch the problem of too few operands to $+$, at a later time.

We can start by using an Abstract Syntax Tree (or AST). An AST is a way of representing the syntactic structure of code. Read <a href="https://en.wikipedia.org/wiki/Abstract_syntax_tree" target="_blank">more about it here</a>. In this tree, the leaf nodes are atomic values, and all the non-leaf nodes are operators. Recursion can naturally be expressed using an AST.

For example, the AST for the expression, $(\+$ $1$ $(\*$ $2$ $3))$ it would look something like this:

[TODO: AST diagram]

This is how we can represent a node of this tree in the code:
{% codeblock astNode.go %}
type ASTNode struct {
  children []*ASTNode // Children of this AST Node.
  isValue  bool       // Checks if this is a value (also if children == nil).  
  value    string
}
{% endcodeblock %}

To actually verify the well-formedness of the expression and build the AST, we would go about it this way:
{% codeblock ast.go %}
// This method gets a list of tokens, and returns:
// 1. The ASTNode of the tree so formed.
// 2. Unused tokens in the end of the array.
// 3. Any error while constructing the tree.
// Removed some error handling to make it a little brief.
func buildAST(tokens []string) (*ASTNode, []string, error) {
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
        childNode, _, err = buildAST([]string{token})
      } else {
        childNode, tokens, err = buildAST(tokens)
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

You can see how the grammar for interpreting the s-expression grammar is hard-coded here. We expect the expression to be either a single value, or something like $($$operator$ $o\_1$ $o\_2$ $...$ $)$, where $o\_i$ can be an atomic value, or a nested expression. They are all `ASTNode` objects, and are returned as part of the `children` slice.

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
Basic evaluation is very simple. We have a struct called `LangEnv`, which is the 'environment' data-structure storing amongst other things, defined operators. When evaluating an AST, if it is a single node, the value of the node is the result. Otherwise, we simply lookup the operator in the environment using `getOperator`, then resolve the operands recursively, and pass the operands to the operator. The operand deals with making sure that the operands are sane.

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

```
func typeCoerce(operatorName string, operands *[]Atom, typePrecendenceMap map[valueType]int)
  (valueType, error)
```

This is what we do inside `typeCoerce`:

1. We get the type : count mapping for all the param values.
2. If there is only one type, there is nothing to do, return the corresponding type. Every value belongs to the same type.
3. If there are multiple types in step 1, pick the one with the highest precedence.
4. Try and cast all operand values to that type. Error out if any of them resists. Because, resistance is futile.

Hence, the $+$ operator would be implemented something like this:
{% codeblock operator.go %}
op :=
  &Operator{
    symbol:      add,
    minArgCount: 2,
    maxArgCount: 100,     // Just an arbit large value.
    handler: func(env *LangEnv, operands []Atom) Atom {
      var retVal Atom
      var finalType valueType
      finalType, retVal.Err = typeCoerce(add, &operands, numValPrecedenceMap)
      if retVal.Err != nil {
        return retVal
      }

      switch finalType {
      case intType:
        var finalVal intValue
        finalVal.value = 0
        for _, o := range operands {
          v, _ := o.Val.(intValue)
          finalVal.value = finalVal.value + v.value
        }
        retVal.Val = finalVal
        break

      case floatType:
        var finalVal floatValue
        finalVal.value = 0
        for _, o := range operands {
          v, _ := o.Val.(floatValue)
          finalVal.value = finalVal.value + v.value
        }
        retVal.Val = finalVal
        break
      }
      return retVal
    },
  }
// Add the operator to the LangEnv's opMap (operator map)
addOperator(env.opMap, op)
{% endcodeblock %}

Here we basically just call `typeCoerce` on the operands, and if its possible to cast them to one single type, we do that casting, and actually perform the addition in the new type.

The $+$ operator can be used to add strings as well. However, we don't want something like $($$+$ $3.14\ \mathrm{"foo"})$. The `typeCoerce` method can be trivially extended to support a list of type valid type precedence maps, and all operands need to belong to the same precedence map. In this case, it could be `{ {intType: 1, floatType: 2}, {stringType: 1 } }`. This particular list ensures that we don't add ints and strings for example, because they don't belong to the same precedence map.

Note that the entire implementation of the operator is defined in the `Operator` struct's `handler` method. Whether or not the operator supports this sort of casting, or decides to roll its own, or not use it at all, is the prerogative of the operator.

## Defining Variables

A typical variable definition could look like this: $(\mathrm{defvar}\ \mathrm{x}\ 3.0)$.

Now, `defvar` is an operator too. It expects the first argument to be of `varType` (matches the regex of a variable), and the value can be anything (except `varType`). We just need to check if the type conditions match, and the variable is not a defined operator. If both are okay, we define the variable in our `LangEnv`'s `varMap`.



 We need to change the part in our `evalAST` method which  to support variable lookup.

{% codeblock eval2.go %}
func evalAST(env *LangEnv, node *ASTNode) Atom {
  // ...
    for i := 1; i < len(node.children); i++ {
      v := evalAST(env, node.children[i])
      if v.Err != nil {
        return v
      }
      // <!-- Lookup code begins
      if v.Val.getValueType() == varType {
        v.Val, v.Err = getVarValue(env, v.Val)
        if v.Err != nil {
          return v
        }
      }
      // Lookup code ends --!>
      operands = append(operands, v)
    }
  // ...
}
{% endcodeblock %}

Here we can assume we have a helper method called `getVarValue`, which looks up the value of a variable in the `varMap`, or throws an error if required (this is also simple to implement).

## Defining Methods

Defining methods is even more fun! We use the `defun` operator. Consider this:

```
(defun circle-area (r) (* 3.14 r r))
```

The first operand is the name of the method, the second is a list of variables that you would pass to the method, and the last is the actual method, assuming that the variables you need are already defined. `(circle-area 10)` after this definition should return `314`.

Calculating the area of a rectangle is pretty much similar.

```
(defun rect-area (x y) (* x y))
```

We need a couple of things for function calls to work fine:

* Create a new `astValue` which can be used for keeping ASTs. So far we were keeping ints, floats and so on.
* Have a way to tell `evalAST` to not evaluate the AST in the `defun` arguments. This is because in `circle-area`, the `(* 3.14 r r)` itself is the value (AST value).
* The `defun` operator needs to add an operator to the `opMap`, with the same name as the method, and define its `handler` method.
* The handler would need expect the same number of params as specified in the definition.
* Till now, our variables have been global in scope. If I do `(defvar x 3.0)`, and then later define a new method as `(defun foo (x) (+ 1 x))`, the interpreter may look at the `varMap` and think that I want to use the global `x`, which is $3.0$. I want to use the one defined as a parameter to the function call. For this, we would need:
  * A new `LangEnv` to be created, inside the `handler`.
  * First copy the same `varMap` as the parent `LangEnv` passed to the handler.
  * Then copy the params passed to the handler. Any duplicates will be overwritten, but all global definitions would be preserved. The function-local scope would take priority.
  * Inside the handler, we will call `evalAST` to evaluate the AST we were provided in the method definition with the new `LangEnv`
  * We also keep track of the recursion depth in `LangEnv`, and it is incremented every time a recursive call is made. If it exceeds a large value (100000 for now), we can error out, so as to salvage the interpreter at least.

This is the only complicated part of the interpreter. Those interested in the code can check it out <a href="https://github.com/reddragon/lambda/blob/master/lang/operator.go#L494" target="_blank">here</a>.

## Recursion

Apart from making sure that we have some sort of recursion depth limit enforced, recursion does not need any special handling. Except, defining some new operators like `cond` (the if-else equivalent), which are required for writing something useful.

Here is the implementation of the factorial function:

```
(defun fact (x)
  (cond                     ; conditional block
    ((= x 0) 1)             ; if x == 0, return 1
    (true                   ; else
      (* x (fact (- x 1)))  ; return x * fact(x - 1)
    )
  )
)
```
`fact(10)` returns `3628800` as expected.

## Porting to iOS

Once I had the interpreter working fine, I wanted to run this on an iOS app. Why? Just for fun. It turns out with Go 1.5, a new tool called <a href="https://godoc.org/golang.org/x/mobile/cmd/gomobile" target="_blank">gomobile</a>. Hana Kim gave a <a href="https://talks.golang.org/2015/gophercon-go-on-mobile.slide#1" target="_blank">talk about this at GopherCon 2015</a>.

What it does is, it compiles your Go package into a static library, and generates Objective-C bindings for it, and wraps them together in a nice iOS friendly `.framework` package.

There are a few restrictions regarding not being able to return complex types such as structs within structs, but apart from that it was fairly easy to use in my bare-bones app. <a href="https://github.com/reddragon/lambda-iOS" target="_blank">Here is the code</a> for the app, and here is a quick demo.
