; ModuleID = "test_014.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

define i32 @"fibonacciRec"(i32 %"n", i32 %".2")
{
entry:
  %"n.1" = alloca i32, align 4
  %"ID" = alloca i32
  %"ID.1" = alloca i32
  %".4" = load i32, i32* %"ID"
  %".5" = load i32, i32* %"ID.1"
  %"add" = add i32 %".4", %".5"
  br label %"exit"
exit:
  %"func_fibonacciRec_return" = add i32 %"n", %".2"
  ret i32 %"func_fibonacciRec_return"
}

define i32 @"fibonacciIter"(i32 %"n", i32 %".2")
{
entry:
  %"n.1" = alloca i32, align 4
  %"k" = alloca i32, align 4
  %"f" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 1, i32* %"i"
  store i32 0, i32* %"f"
  store i32 1, i32* %"k"
  br label %"repeat_start"
repeat_start:
  %"1" = alloca i32
  %".8" = load i32, i32* %"1"
  %".9" = load i32, i32* %"k"
  %"increment" = add i32 %".9", %".8"
  %".10" = load i32, i32* %"k"
  call void @"escrevaInteiro"(i32 %".10")
  br label %"exit"
repeat_end:
exit:
  %"func_return" = load i32, i32* %"f", align 4
  ret i32 %"func_return"
}

define i32 @"main"()
{
entry:
  %".2" = call i32 @"leiaInteiro"()
  store i32 %".2", i32* %"n.1"
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"n.1"
  store i32 1, i32* %"i"
  br label %"repeat_start"
repeat_start:
  %"1" = alloca i32
  %".8" = load i32, i32* %"1"
  %".9" = load i32, i32* %"i"
  %"increment" = add i32 %".9", %".8"
  %".10" = load i32, i32* %"i"
  call void @"escrevaInteiro"(i32 %".10")
  store i32 1, i32* %"i"
  br label %"repeat_start.1"
repeat_end:
repeat_start.1:
  %"1.1" = alloca i32
  %".14" = load i32, i32* %"1.1"
  %".15" = load i32, i32* %"i"
  %"increment.1" = add i32 %".15", %".14"
  %".16" = load i32, i32* %"i"
  call void @"escrevaInteiro"(i32 %".16")
  br label %"exit"
repeat_end.1:
exit:
  ret i32 0
}
