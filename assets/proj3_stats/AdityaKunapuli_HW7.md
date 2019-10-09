    df <- read.csv("http://www.faculty.ucr.edu/~jflegal/fish.txt", sep=" ")

***Problem 1***
===============

    bh <- function(B1, B2)
    {
      return(1/(B1+B2/df$S))
    }
    plot(df$S, bh(1,3), xlab="S", ylab="R", col="black", ylim=c(0,1), pch=20)
    points(df$S, bh(1,500), xlab="S", ylab="R", col="red", pch=20)
    # plot(R~S, data=df, bh(1/z$a,z$b/z$b), xlab="S", ylab="R", col="blue", pch=20)
    # plot(df$S, bh2(z$a,z$b), xlab="S", ylab="R", col="blue", pch=20)
    points(df$S, bh(2,100), xlab="S", ylab="R", col="green", pch=20)
    points(df$S, bh(2,10), xlab="S", ylab="R", col="purple", pch=20)
    points(df$S, bh(3,1), xlab="S", ylab="R", col="pink", pch=20)

![](AdityaKunapuli_HW7_files/figure-markdown_strict/unnamed-chunk-2-1.png)

***Problem 2***
===============

    bhlin <- function(B1, B2)
    {
      return(B1+(B2/df$S))
    }

    lm(bhlin(1,500)~1/df$S, data=df)

    ## 
    ## Call:
    ## lm(formula = bhlin(1, 500) ~ 1/df$S, data = df)
    ## 
    ## Coefficients:
    ## (Intercept)  
    ##       3.726

    lm(1/df$S~1/df$R)

    ## 
    ## Call:
    ## lm(formula = 1/df$S ~ 1/df$R)
    ## 
    ## Coefficients:
    ## (Intercept)  
    ##    0.005452

    lm(bhlin(1,500)~(1/df$S))

    ## 
    ## Call:
    ## lm(formula = bhlin(1, 500) ~ (1/df$S))
    ## 
    ## Coefficients:
    ## (Intercept)  
    ##       3.726

    xavg <- mean(1/df$S)
    yavg <- mean(bhlin(1,500))
    m <- sum(((1/df$S)-xavg)*(bhlin(1,500)-yavg))/sum(((1/df$S)-xavg)^2)
    b <- yavg - m*xavg

    xRan <- seq(0.00,0.02, by = 0.0001)
    plot(1/df$S, bhlin(1,500), xlab="1/S", ylab="1/R", col="red", pch=16)
    lines(xRan,(m*xRan+b))

![](AdityaKunapuli_HW7_files/figure-markdown_strict/unnamed-chunk-3-1.png)

***Problem 3***
===============

### Stable population occurs when S = 130 and S = 400

***Problem 4***
===============

    library(FSA)

    ## ## FSA v0.8.22. See citation('FSA') if used in publication.
    ## ## Run fishR() for related website and fishR('IFAR') for related book.

    library(boot)
    z <- srStarts(R~S,data=df,type="BevertonHolt",param=1)

    rsq <- function(formula, data, indices) {
      d <- data[indices,]  
      fit <- lm(formula, data=d)
      return(summary(fit)$r.square)
    } 

    results <- boot(data=df, statistic=rsq, R=1000, formula=R~S)
    results

    ## 
    ## ORDINARY NONPARAMETRIC BOOTSTRAP
    ## 
    ## 
    ## Call:
    ## boot(data = df, statistic = rsq, R = 1000, formula = R ~ S)
    ## 
    ## 
    ## Bootstrap Statistics :
    ##      original        bias    std. error
    ## t1* 0.8973988 -0.0004321788  0.02717934

    boot.ci(results, type="bca")

    ## BOOTSTRAP CONFIDENCE INTERVAL CALCULATIONS
    ## Based on 1000 bootstrap replicates
    ## 
    ## CALL : 
    ## boot.ci(boot.out = results, type = "bca")
    ## 
    ## Intervals : 
    ## Level       BCa          
    ## 95%   ( 0.8316,  0.9411 )  
    ## Calculations and Intervals on Original Scale

    plot(results)

![](AdityaKunapuli_HW7_files/figure-markdown_strict/unnamed-chunk-4-1.png)

    df2 <- read.csv("http://www.faculty.ucr.edu/~jflegal/buffalo.txt")
    df2 <- as.numeric(df2[[1]])
    d1 <- density(df2, kernel = "epanechnikov")
    d2 <- density(df2, kernel = "gaussian")
    plot(d2, col="red", main="Kernel Density")
    lines(d1, col="blue")

![](AdityaKunapuli_HW7_files/figure-markdown_strict/unnamed-chunk-5-1.png)

***Problem 7***
===============

### Increasing the bandwidth for either kernel type smoothed out the plot and reduced the number of buckets appearing.

    d3 <- density(df2, kernel = "epanechnikov", bw=1)
    d4 <- density(df2, kernel = "epanechnikov", bw=9)
    d5 <- density(df2, kernel = "gaussian", bw = 1)
    d6 <- density(df2, kernel = "gaussian", bw = 9)
    plot(d5, col="red", main="Kernel Density", lty=3, xlab="")
    lines(d6, col="red", lty=1)
    lines(d4, col="darkgreen", lty=2, lwd=2)
    lines(d3, col="blue", lty=3)

![](AdityaKunapuli_HW7_files/figure-markdown_strict/unnamed-chunk-6-1.png)
