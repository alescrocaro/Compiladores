; ModuleID = "test_010.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

@"n" = common global i32 0, align 4
define i32 @"fatorial"(i32 %"n", i32 %".2")
{
entry:
  %"n.1" = alloca i32, align 4
  %"fat" = alloca i32, align 4
  br label %"exit"
exit:
  %"func_fatorial_return" = add i32 %"n", %".2"
  ret i32 %"func_fatorial_return"
}

define i32 @"main"()
{
entry:
  %".2" = call i32 @"leiaInteiro"()
  store i32 %".2", i32* @"n"
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"n.1"
  br label %"exit"
exit:
  ret i32 0
}
