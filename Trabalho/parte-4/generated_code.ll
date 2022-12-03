; ModuleID = "test.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

define i32 @"soma"(i32 %"b", i32 %"a")
{
entry:
  %"b.1" = alloca i32, align 4
  %"a.1" = alloca i32, align 4
  %"a.2" = alloca i32
  %"b.2" = alloca i32
  %".4" = load i32, i32* %"a.2"
  %".5" = load i32, i32* %"b.2"
  %"add" = add i32 %".4", %".5"
  br label %"exit"
exit:
  %"func_soma_return" = add i32 %"b", %"a"
  ret i32 %"func_soma_return"
}

define i32 @"main"()
{
entry:
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"repeat_start"
repeat_start:
  %".4" = load i32, i32* %"i"
  %"atrib_expression_result" = add i32 %".4", 1
  store i32 %"atrib_expression_result", i32* %"i"
  %"1" = alloca i32
  %".6" = load i32, i32* %"1"
  %".7" = load i32, i32* %"i"
  %"increment" = add i32 %".7", %".6"
  %".8" = load i32, i32* %"i"
  call void @"escrevaInteiro"(i32 %".8")
  %".10" = call i32 @"leiaInteiro"()
  store i32 %".10", i32* %"b.1"
  %".12" = call i32 @"leiaInteiro"()
  store i32 %".12", i32* %"b"
  %".14" = call i32 @"leiaInteiro"()
  store i32 %".14", i32* %"a.1"
  %".16" = call i32 @"leiaInteiro"()
  store i32 %".16", i32* %"a"
  %"b_cmp" = load i32, i32* %"i", align 4
  %"repeat_until_check" = icmp eq i32 %"b_cmp", 5
  br i1 %"repeat_until_check", label %"repeat_start", label %"repeat_end"
repeat_end:
  br label %"exit"
exit:
  ret i32 0
}
