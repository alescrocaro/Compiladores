; ModuleID = "test_015.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

define i32 @"func"(i32 %"p2", i32 %"p1")
{
entry:
  %"p2.1" = alloca i32, align 4
  %"p1.1" = alloca i32, align 4
  %"r" = alloca i32, align 4
  %".4" = load i32, i32* %"p1.1"
  %".5" = load i32, i32* %"p2.1"
  %"atrib_expression_result" = add i32 %".4", %".5"
  store i32 %"atrib_expression_result", i32* %"r"
  br label %"exit"
exit:
  %"func_return" = load i32, i32* %"r", align 4
  ret i32 %"func_return"
}

define i32 @"main"()
{
entry:
  %"x" = alloca i32, align 4
  %".2" = load i32, i32* %"x"
  call void @"escrevaInteiro"(i32 %".2")
  br label %"exit"
exit:
  ret i32 0
}
