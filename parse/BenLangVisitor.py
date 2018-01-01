# Generated from BenLang.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BenLangParser import BenLangParser
else:
    from BenLangParser import BenLangParser

# This class defines a complete generic visitor for a parse tree produced by BenLangParser.

class BenLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BenLangParser#statement.
    def visitStatement(self, ctx:BenLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#statementBlock.
    def visitStatementBlock(self, ctx:BenLangParser.StatementBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#prog.
    def visitProg(self, ctx:BenLangParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#aType.
    def visitAType(self, ctx:BenLangParser.ATypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#declaration.
    def visitDeclaration(self, ctx:BenLangParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#assignment.
    def visitAssignment(self, ctx:BenLangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#whileLoop.
    def visitWhileLoop(self, ctx:BenLangParser.WhileLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#ifElse.
    def visitIfElse(self, ctx:BenLangParser.IfElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#ifOnly.
    def visitIfOnly(self, ctx:BenLangParser.IfOnlyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#expr.
    def visitExpr(self, ctx:BenLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#application.
    def visitApplication(self, ctx:BenLangParser.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#params.
    def visitParams(self, ctx:BenLangParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BenLangParser#paramsRest.
    def visitParamsRest(self, ctx:BenLangParser.ParamsRestContext):
        return self.visitChildren(ctx)



del BenLangParser