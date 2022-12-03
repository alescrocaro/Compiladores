; ModuleID = "test_003.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

@"a" = common global i32 0, align 4
define i32 @"main"()
{
entry:
  %"ret" = alloca i32, align 4
  store i32 25, i32* @"a"
  br label %"exit"
exit:
  %"func_return" = load i32, i32* %"ret", align 4
  ret i32 %"func_return"
}
