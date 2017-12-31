# Generated from BenLang.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BenLangParser import BenLangParser
else:
    from BenLangParser import BenLangParser

# This class defines a complete listener for a parse tree produced by BenLangParser.
class BenLangListener(ParseTreeListener):

    # Enter a parse tree produced by BenLangParser#statement.
    def enterStatement(self, ctx:BenLangParser.StatementContext):
        pass

    # Exit a parse tree produced by BenLangParser#statement.
    def exitStatement(self, ctx:BenLangParser.StatementContext):
        pass


    # Enter a parse tree produced by BenLangParser#expression.
    def enterExpression(self, ctx:BenLangParser.ExpressionContext):
        pass

    # Exit a parse tree produced by BenLangParser#expression.
    def exitExpression(self, ctx:BenLangParser.ExpressionContext):
        pass


    # Enter a parse tree produced by BenLangParser#statementBlock.
    def enterStatementBlock(self, ctx:BenLangParser.StatementBlockContext):
        pass

    # Exit a parse tree produced by BenLangParser#statementBlock.
    def exitStatementBlock(self, ctx:BenLangParser.StatementBlockContext):
        pass


    # Enter a parse tree produced by BenLangParser#prog.
    def enterProg(self, ctx:BenLangParser.ProgContext):
        pass

    # Exit a parse tree produced by BenLangParser#prog.
    def exitProg(self, ctx:BenLangParser.ProgContext):
        pass


    # Enter a parse tree produced by BenLangParser#declaration.
    def enterDeclaration(self, ctx:BenLangParser.DeclarationContext):
        pass

    # Exit a parse tree produced by BenLangParser#declaration.
    def exitDeclaration(self, ctx:BenLangParser.DeclarationContext):
        pass


    # Enter a parse tree produced by BenLangParser#assignment.
    def enterAssignment(self, ctx:BenLangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by BenLangParser#assignment.
    def exitAssignment(self, ctx:BenLangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by BenLangParser#whileLoop.
    def enterWhileLoop(self, ctx:BenLangParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by BenLangParser#whileLoop.
    def exitWhileLoop(self, ctx:BenLangParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by BenLangParser#ifElse.
    def enterIfElse(self, ctx:BenLangParser.IfElseContext):
        pass

    # Exit a parse tree produced by BenLangParser#ifElse.
    def exitIfElse(self, ctx:BenLangParser.IfElseContext):
        pass


    # Enter a parse tree produced by BenLangParser#ifOnly.
    def enterIfOnly(self, ctx:BenLangParser.IfOnlyContext):
        pass

    # Exit a parse tree produced by BenLangParser#ifOnly.
    def exitIfOnly(self, ctx:BenLangParser.IfOnlyContext):
        pass


    # Enter a parse tree produced by BenLangParser#expr.
    def enterExpr(self, ctx:BenLangParser.ExprContext):
        pass

    # Exit a parse tree produced by BenLangParser#expr.
    def exitExpr(self, ctx:BenLangParser.ExprContext):
        pass


    # Enter a parse tree produced by BenLangParser#application.
    def enterApplication(self, ctx:BenLangParser.ApplicationContext):
        pass

    # Exit a parse tree produced by BenLangParser#application.
    def exitApplication(self, ctx:BenLangParser.ApplicationContext):
        pass


    # Enter a parse tree produced by BenLangParser#params.
    def enterParams(self, ctx:BenLangParser.ParamsContext):
        pass

    # Exit a parse tree produced by BenLangParser#params.
    def exitParams(self, ctx:BenLangParser.ParamsContext):
        pass


    # Enter a parse tree produced by BenLangParser#paramsRest.
    def enterParamsRest(self, ctx:BenLangParser.ParamsRestContext):
        pass

    # Exit a parse tree produced by BenLangParser#paramsRest.
    def exitParamsRest(self, ctx:BenLangParser.ParamsRestContext):
        pass


