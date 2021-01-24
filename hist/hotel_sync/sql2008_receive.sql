USE [xghotel]
GO

/****** Object:  Table [dbo].[receive]    Script Date: 01/23/2021 16:53:50 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[receive](
	[roomno] [nvarchar](20) NULL,
	[id] [nvarchar](50) NOT NULL,
	[tgno] [nvarchar](50) NULL,
	[orno] [nvarchar](50) NULL,
	[groupno] [nvarchar](50) NULL,
	[name] [nvarchar](20) NULL,
	[sex] [nvarchar](6) NULL,
	[birt] [datetime] NULL,
	[gutp] [nvarchar](50) NULL,
	[the_class] [nvarchar](20) NULL,
	[what_card] [nvarchar](20) NULL,
	[cardno] [nvarchar](50) NULL,
	[city] [nvarchar](20) NULL,
	[addr] [nvarchar](100) NULL,
	[tele] [nvarchar](20) NULL,
	[the_date] [smalldatetime] NULL,
	[the_time] [datetime] NULL,
	[days] [money] NULL,
	[price] [money] NULL,
	[leave_date] [smalldatetime] NULL,
	[money_less] [money] NULL,
	[all_money] [money] NULL,
	[bed_type] [nvarchar](20) NULL,
	[bed_num] [money] NULL,
	[money_fact] [money] NULL,
	[bed_money] [money] NULL,
	[the_man] [nvarchar](10) NULL,
	[bed_date] [smalldatetime] NULL,
	[leave_flag] [nvarchar](10) NULL,
	[hour] [money] NULL,
	[leave_time] [smalldatetime] NULL,
	[pay_class] [nvarchar](50) NULL,
	[pay_flag] [nvarchar](10) NULL,
	[iccard_class] [nvarchar](50) NULL,
	[iccard_no] [nvarchar](50) NULL,
	[per] [money] NULL,
	[give_money] [money] NULL,
	[man_num] [money] NULL,
	[count_date] [smalldatetime] NULL,
	[counter] [int] NULL,
	[normal_price] [money] NULL,
	[ser_money] [money] NULL,
	[dateman] [nvarchar](20) NULL,
	[hman_flag] [nvarchar](50) NULL,
	[memo] [nvarchar](255) NULL,
	[give_class] [nvarchar](20) NULL,
	[per_man] [nvarchar](50) NULL,
	[room_class] [nvarchar](20) NULL,
	[hour_price] [money] NULL,
	[hour_flag] [nvarchar](20) NULL,
	[the_company] [nvarchar](50) NULL,
	[receive_class] [nvarchar](20) NULL,
	[print_flag] [nvarchar](20) NULL,
	[print_time] [smalldatetime] NULL,
	[group_id] [nvarchar](50) NULL,
	[leave_man] [nvarchar](50) NULL,
	[fj_money] [nvarchar](50) NULL,
	[memo1] [nvarchar](200) NULL,
	[night_flag] [nvarchar](50) NULL,
	[invno] [nvarchar](50) NULL,
	[invno_money] [money] NULL,
	[will_leave] [smalldatetime] NULL,
	[invno_seq] [int] NULL,
	[floor] [nvarchar](50) NULL,
	[moveto_id] [nvarchar](50) NULL,
	[hour_flagdo] [nvarchar](50) NULL,
	[the_position] [nvarchar](50) NULL,
	[seq] [int] NULL,
	[man_needhome] [nvarchar](50) NULL,
	[man_love] [nvarchar](50) NULL,
	[man_professinon] [nvarchar](50) NULL,
	[entry_port] [nvarchar](50) NULL,
	[visa_type] [nvarchar](50) NULL,
	[now_staying] [nvarchar](50) NULL,
	[where_from] [nvarchar](50) NULL,
	[where_go] [nvarchar](50) NULL,
	[entry_date] [smalldatetime] NULL,
	[home_address] [nvarchar](50) NULL,
	[object_stay] [nvarchar](50) NULL,
	[validity_stay] [smalldatetime] NULL,
	[host_company] [nvarchar](50) NULL,
	[hmt_flag] [nvarchar](50) NULL,
	[uncheckout_flag] [nvarchar](50) NULL,
	[certi_valid] [smalldatetime] NULL,
	[break_first] [int] NULL,
	[link_id] [nvarchar](50) NULL,
	[dateman_date] [smalldatetime] NULL,
	[dateman_leave_date] [smalldatetime] NULL,
	[ct_flag] [nvarchar](50) NULL,
	[receive_flag] [nvarchar](50) NULL,
	[billid] [nvarchar](200) NULL,
	[select_flag] [bit] NULL,
	[sfz_flag] [bit] NULL,
	[txdate] [smalldatetime] NULL,
	[txflag] [bit] NULL,
	[fpflag] [bit] NULL,
	[xsname] [nvarchar](50) NULL,
	[fpflag1] [bit] NULL,
	[nightday] [int] NULL,
	[fpinvno] [nvarchar](50) NULL,
	[hourslen] [int] NULL,
	[gzcompany] [nvarchar](50) NULL,
	[jsfs] [bit] NULL,
	[checkroomdate] [datetime] NULL,
	[make_date] [datetime] NULL,
	[make_time] [datetime] NULL,
	[mastbill_flag] [bit] NULL,
	[bookid] [nvarchar](50) NULL,
	[ssyflag] [bit] NULL,
	[zzzdate] [nvarchar](10) NULL,
	[weixinflag] [bit] NULL,
	[weixin] [nvarchar](50) NULL,
	[prints] [int] NULL,
	[zcnum] [int] NULL,
	[mz] [nvarchar](50) NULL,
 CONSTRAINT [PK_receive] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_hour_price]  DEFAULT (0) FOR [hour_price]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_break_first]  DEFAULT (0) FOR [break_first]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_billid]  DEFAULT ('') FOR [billid]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_select_flag]  DEFAULT (1) FOR [select_flag]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_sfz_flag]  DEFAULT (0) FOR [sfz_flag]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_txflag]  DEFAULT (0) FOR [txflag]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_fpflag]  DEFAULT (1) FOR [fpflag]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_fpflag1]  DEFAULT (0) FOR [fpflag1]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_nightday]  DEFAULT (0) FOR [nightday]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF_receive_hourslen]  DEFAULT (0) FOR [hourslen]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF__receive__jsfs__36DC0ACC]  DEFAULT (1) FOR [jsfs]
GO

ALTER TABLE [dbo].[receive] ADD  CONSTRAINT [DF__receive__mastbil__11FF8BD8]  DEFAULT (0) FOR [mastbill_flag]
GO

ALTER TABLE [dbo].[receive] ADD  DEFAULT (0) FOR [ssyflag]
GO

ALTER TABLE [dbo].[receive] ADD  DEFAULT ('1900') FOR [zzzdate]
GO

ALTER TABLE [dbo].[receive] ADD  DEFAULT (0) FOR [weixinflag]
GO

