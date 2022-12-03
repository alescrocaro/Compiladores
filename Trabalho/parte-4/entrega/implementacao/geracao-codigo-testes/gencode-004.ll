; ModuleID = "test_004.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

@"n" = common global i32 0, align 4
@"soma" = common global i32 0, align 4
define i32 @"main"()
{
entry:
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  br label %"repeat_start"
repeat_start:
  %"1" = alloca i32
  %".5" = load i32, i32* %"1"
  %".6" = load i32, i32* @"n"
  %"decrement" = sub i32 %".6", %".5"
  %"b_cmp" = load i32, i32* @"n", align 4
  %"repeat_until_check" = icmp eq i32 %"b_cmp", 0
  br i1 %"repeat_until_check", label %"repeat_start", label %"repeat_end"
repeat_end:
  %".8" = load i32, i32* @"soma"
  call void @"escrevaInteiro"(i32 %".8")
  br label %"exit"
exit:
  ret i32 0
}
