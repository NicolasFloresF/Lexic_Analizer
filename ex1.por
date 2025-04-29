programa {
  funcao inicio() {
    inteiro a = -10
    inteiro b = +20, e, f = 10, g 
    inteiro c = a + b
    inteiro d
    c = 4
    leia(g)
    escreva(c)
    escreva("Hello World")
    se (39.37 + 4 - 5 * 10 != 6.36 - 4){
      escreva("Inside IF statement")
      d--
    }
    senao{
      escreva("Inside ELSE statement")
      d++
    }
    enquanto (d < 10){
      escreva(d)
      d++
    }
    teste(a, b, c)
  }

  funcao teste(inteiro i, inteiro j, inteiro k) {
    inteiro a = -10
    inteiro b = +20, e, f = 10, g 
    inteiro c = a + b
    inteiro d
    logico log = verdadeiro
    para(i = 0;i < 10;i++){
      escreva(i)
    }
    
    retorne i + j + k
  }
}
