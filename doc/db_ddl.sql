
CREATE TABLE [csidbo].[FTPart_Stock_Product_Property_1](
	[PropertyID] [int] IDENTITY(1,1) NOT NULL,
	[MainID] [int] NOT NULL,
	[ExtendID] [int] NOT NULL,
	[_SelfImageType] [int] NOT NULL,
	[_ImageID] [int] NOT NULL,
	[_LineColor] [int] NOT NULL,
	[其它.应采购价] [dbo].[小数_金额] NULL,
	[其它.货物状态] [nvarchar](510) NULL,
	[其它.业务员] [dbo].[字符_20] NULL,
	[其它.商品品牌] [nvarchar](510) NULL,
	[其它.单价] [dbo].[小数_金额] NULL,
	[其它.报价币种] [nvarchar](510) NULL,
	[其它.供应商名称] [dbo].[客户选择] NULL,
	[_其它.供应商名称] [dbo].[_客户选择] NULL,
	[其它.采购剩余数量] [dbo].[整数] NULL,
	[其它.已出库数量] [dbo].[整数] NULL,
	[其它.允采购量] [dbo].[整数] NULL,
	[其它.销售合同数量] [dbo].[整数] NULL,
PRIMARY KEY CLUSTERED
(
	[PropertyID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT (0) FOR [ExtendID]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT (0) FOR [_SelfImageType]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [_ImageID]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [_LineColor]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [其它.应采购价]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  CONSTRAINT [DF__FTPart_St__其它.货物__3B795FF2]  DEFAULT ('新单') FOR [其它.货物状态]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ('') FOR [其它.业务员]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [其它.单价]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [_其它.供应商名称]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [其它.采购剩余数量]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [其它.已出库数量]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [其它.允采购量]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Product_Property_1] ADD  DEFAULT ((0)) FOR [其它.销售合同数量]
GO




CREATE TABLE [csidbo].[FTPart_Stock_Property_1](
	[PropertyID] [int] IDENTITY(1,1) NOT NULL,
	[MainID] [int] NOT NULL,
	[ExtendID] [int] NOT NULL,
	[_SelfImageType] [int] NOT NULL,
	[_ImageID] [int] NOT NULL,
	[_LineColor] [int] NOT NULL,
	[_PrintNum] [int] NOT NULL,
	[_FaxNum] [int] NOT NULL,
	[_EmailNum] [int] NOT NULL,
	[_CheckResult] [int] NOT NULL,
	[美元汇率] [dbo].[小数_金额] NULL,
	[欧元汇率] [dbo].[小数_金额] NULL,
	[采购利润比] [dbo].[百分比] NULL,
	[采购人] [dbo].[用户选择] NULL,
	[采购别名] [dbo].[字符_50] NULL,
	[测试] [dbo].[百分比] NULL,
PRIMARY KEY CLUSTERED
(
	[PropertyID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT (0) FOR [ExtendID]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT (0) FOR [_SelfImageType]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [_ImageID]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [_LineColor]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [_PrintNum]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [_FaxNum]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [_EmailNum]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [_CheckResult]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [美元汇率]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ((0)) FOR [欧元汇率]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ('10') FOR [采购利润比]
GO

ALTER TABLE [csidbo].[FTPart_Stock_Property_1] ADD  DEFAULT ('') FOR [采购别名]
GO

